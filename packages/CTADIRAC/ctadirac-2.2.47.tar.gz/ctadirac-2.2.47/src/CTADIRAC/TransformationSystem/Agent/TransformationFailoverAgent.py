import concurrent.futures
from collections import defaultdict
from typing import Any, Union
from rich.table import Table
from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Utilities.ReturnValues import DOKReturnType, DErrorReturnType
from DIRAC.Core.Base.AgentModule import AgentModule

from DIRAC.TransformationSystem.Client import (
    TransformationStatus,
    TransformationFilesStatus,
)
from DIRAC.WorkloadManagementSystem.Client.JobMonitoringClient import (
    JobMonitoringClient,
)
from DIRAC.WorkloadManagementSystem.Client import JobStatus
from DIRAC.TransformationSystem.DB.TransformationDB import TransformationDB
from CTADIRAC.TransformationSystem.Utils.FailoverUtilities import FailoverUtilities
from CTADIRAC.Core.Utilities.return_values import s_report

AGENT_NAME = "Transformation/TransformationFailoverAgent"


class TransformationFailoverAgent(AgentModule, FailoverUtilities):
    """TransformationFailoverAgent:
    An Agent to manage failovers during Transformations
    Sends report, reassign files, complete or flush transfomations depending on configuration.
    Need a specific configuration for the agent:
    - TransformationStatus: Check the transformations with specific status (default: 'Active')
    - TransformationTypes: Check the transformations with specific types (default: None)
    - TypesToReport: Transformation type to report (default == TransformationTypes)
    - Complete: Complete transformation with specified type if conditions (default: None)
    - Flush: Flush transformation with specified type if conditions (default: None)
    - Reschedule: Reassigned files to create new tasks when there is failed tasks in the transformation with specified type (default: None)
    - MaxReassign: Maximum number of reassigning files (default: 2)
    - maxThreadsInPool: Number of threads used by the agent
    - MailTo: Send report to sepcified mail adress
    """

    def __init__(self, *args, **kwargs) -> None:
        AgentModule.__init__(self, *args, **kwargs)
        FailoverUtilities.__init__(self, agent_name=AGENT_NAME)

        self.trigger_job_status: list[str] = [JobStatus.FAILED, JobStatus.KILLED]
        self.failed_final_task_status: list[str] = [JobStatus.FAILED, JobStatus.KILLED]
        self.default_transformation_status: list[str] = [TransformationStatus.ACTIVE]
        self.file_status_to_check = TransformationFilesStatus.ASSIGNED
        self.trans_with_no_input: list = ["MCSimulation"]

        self.job_mon = JobMonitoringClient()
        self.trans_db = TransformationDB()
        self.get_cs_options()

        self.mail_to = ""
        self.mail_from = "noreply@dirac.system"
        self.subject = "[TransformationFailoverAgent]"

        self.attributes_of_interest: list[str] = [
            "Status",
            "MinorStatus",
            "ApplicationStatus",
            "Site",
        ]
        self.html = False
        self.reassign_count = {}

    def initialize(self) -> DOKReturnType[None]:
        """Agent's initialisation"""
        self.mail_from = self.am_getOption("MailFrom", self.mail_from)
        self.mail_to = self.am_getOption("MailTo", self.mail_to)

        max_number_of_threads = self.am_getOption("maxThreadsInPool", 15)
        gLogger.info(f"Multithreaded with {max_number_of_threads} threads")
        self.thread_pool_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_number_of_threads
        )
        return S_OK()

    def get_cs_options(self) -> None:
        """Re initialize before execution"""
        self.html = self.am_getOption("htmlReport", False)
        self.transformation_status = self.am_getOption(
            "TransformationStatus", self.default_transformation_status
        )

        self.transformation_types = self.am_getOption("TransformationTypes", [])
        self.transformation_to_report = self.am_getOption(
            "TypesToReport", self.transformation_types
        )
        self.transformations_to_complete = self.am_getOption("Complete", [])
        self.transformation_to_flush = self.am_getOption("Flush", [])
        self.transformation_to_reschedule = self.am_getOption("Reschedule", [])

        self.max_reassign = self.am_getOption("MaxReassign", 2)

    """
    Core methods:
    """

    def should_complete_transformation(
        self, trans_type: str, trans_id: int, parent_id: int
    ) -> bool:
        """Check if transformation should be completed.
        i.e. has input, is processed and has no parent
        or parent is processed"""
        not_completed_message: str = (
            f"[{trans_id}] Do not complete transformation: requirement not satisfied"
        )
        if (
            trans_type in self.trans_with_no_input
            or trans_type not in self.transformations_to_complete
            or parent_id is None
        ):
            gLogger.info(not_completed_message)
            return False

        if self.is_transformation_processed(trans_id) and (
            parent_id == -1
            or (parent_id != -1 and self.is_transformation_processed(parent_id))
            or (parent_id != -1 and self.get_parent_type(parent_id) == "MCSimulation")
        ):
            gLogger.info(f"[{trans_id}] Completing transformation...")
            return True

        gLogger.info(not_completed_message)
        return False

    def check_transformation(
        self, trans_id: int, trans_info_dict: dict
    ) -> Union[DOKReturnType[dict], DErrorReturnType, Any]:
        """Check transformation before creating a report
        if necessary flush and reassign files"""
        gLogger.info(f"[{trans_id}] Checking Transformation:")

        trans_type = trans_info_dict["Type"]
        parent_id = self.get_parent_transformation_id(trans_id)
        reassigned_lfns: dict = {}
        no_report: str = f"[{trans_id}] Report not created"

        tasks_infos = self.get_transformation_tasks(trans_id)["Value"]
        if not tasks_infos:
            return s_report(False, f"{no_report}: empty transformation")

        if (
            trans_type not in self.trans_with_no_input
            and self.is_transformation_processed(trans_id)
        ):
            return s_report(False, f"[{trans_id}] is processed")

        # Do nothing if all files are processed and complete transformation:
        if self.should_complete_transformation(trans_type, trans_id, parent_id):
            return self.complete_transformation(trans_id)

        jobs_id: list = [
            job["ExternalID"] for job in tasks_infos if job["ExternalID"] != "0"
        ]
        res_jobs_attributes = self.job_mon.getJobsParameters(
            jobs_id, self.attributes_of_interest
        )
        if not res_jobs_attributes["OK"]:
            return s_report(False, f"{res_jobs_attributes}")

        jobs_attributes: dict = res_jobs_attributes["Value"]

        self.update_tasks_status(jobs_attributes, tasks_infos)

        # Check if transformation needs to be flushed
        if trans_type in self.transformation_to_flush:
            self.flush_transformation(trans_id, trans_info_dict, parent_id)

        # Set files status to unused if associated tasks failed or killed
        if trans_type in self.transformation_to_reschedule:
            # TODO: Send mail with reassign files number
            reassigned_lfns = self.reassign_lfn(trans_id)

        if trans_type not in self.transformation_to_report:
            return s_report(
                False, f"{no_report}: {trans_type} type should not be reported"
            )

        # Create Report on transformation
        report_result = self.parse_transformation_jobs_attributes(
            trans_id, jobs_attributes
        )

        if not report_result["OK"]:
            return report_result

        if reassigned_lfns:
            report_lfns: str = self.create_reassigned_lfn_report(
                trans_id, reassigned_lfns
            )
            return s_report(True, report_result["Value"] + report_lfns)

        return s_report(True, report_result["Value"])

    def update_tasks_status(self, jobs_attributes, tasks_infos):
        """Update task status in TransformationDB"""
        tasks_status_dict = {}
        for task in tasks_infos:
            tasks_status_dict[task["ExternalID"]] = {
                "ExternalStatus": task["ExternalStatus"],
                "TransformationID": task["TransformationID"],
                "TaskID": task["TaskID"],
            }
        for job_id, job_info in jobs_attributes.items():
            try:
                if tasks_status_dict[job_id]["ExternalStatus"] != job_info["Status"]:
                    res = self.trans_db.setTaskStatus(
                        tasks_status_dict[job_id]["TransformationID"],
                        tasks_status_dict[job_id]["TaskID"],
                        job_info["Status"],
                    )
                    if not res["OK"]:
                        continue
            except KeyError:
                continue

    def get_lfns_to_assign(self, trans_id: int, failed_tasks: list) -> dict:
        """Get LFNs to assign based on failed tasks"""
        lfns_to_assign = {}
        res_trans_files = self.get_transformation_files(
            condDict={"TaskID": failed_tasks}
        )
        if res_trans_files["OK"]:
            for trans_file in res_trans_files["Value"]:
                lfn = trans_file["LFN"]
                if (
                    lfn not in self.reassign_count
                    or self.reassign_count[lfn] <= self.max_reassign
                ):
                    lfns_to_assign[trans_file["TaskID"]] = lfn
                    self.update_reassign_count(lfn)
            gLogger.info(
                f"[{trans_id}] Change files status to unused on lnfs: {lfns_to_assign}"
            )
        else:
            gLogger.error(
                f"[{trans_id}] Failed to getTransformationFiles: {res_trans_files}"
            )
        return lfns_to_assign

    def update_reassign_count(self, lfn: str) -> None:
        """Update reassign count for the specified LFN"""
        if lfn in self.reassign_count:
            self.reassign_count[lfn] += 1
        else:
            self.reassign_count[lfn] = 1

    def reassign_lfn(self, trans_id: int) -> dict:
        """Set LFNs to Unused if failed or killed tasks"""
        lfns_to_assign: dict = {}
        res_assigned_tasks_status = self.trans_client.get_tasks_by_file_status(
            trans_id, self.file_status_to_check, self.failed_final_task_status
        )
        if res_assigned_tasks_status["OK"]:
            failed_tasks = res_assigned_tasks_status["Value"]
            if failed_tasks:
                lfns_to_assign = self.get_lfns_to_assign(trans_id, failed_tasks)
                res = self.trans_client.setFileStatusForTransformation(
                    trans_id,
                    newLFNsStatus="Unused",
                    lfns=list(lfns_to_assign.values()),
                    force=True,
                )
                if not res["OK"]:
                    gLogger.error(f"[{trans_id}] {res}")
        else:
            gLogger.error(f"{trans_id}: {res_assigned_tasks_status}")

        return lfns_to_assign

    def create_reassigned_lfn_report(self, trans_id: int, lfns_to_assign: dict) -> str:
        """Create report on reassigned files"""
        table: Table = self.init_rich_table(
            title=f"Reassigned LFNs on transformation {trans_id}:",
            fields=["taskID", "lfn"],
        )
        for taskid in lfns_to_assign:
            table.add_row([taskid, lfns_to_assign[taskid]])
        return self.generate_table(table)

    def flush_transformation(
        self, trans_id: int, trans_info_dict: dict, parent_id: int
    ) -> Union[Any, DOKReturnType[dict], DErrorReturnType, None]:
        """Flush transfromation if filled necessary conditions"""
        count_unused = 0
        flush_trans = True
        parent_status = None

        group_size = trans_info_dict["GroupSize"]
        res_parent_trans = self.trans_client.getTransformation(parent_id)
        if res_parent_trans["OK"]:
            parent_status = res_parent_trans["Value"]["Status"]

        if parent_id != -1 and parent_status != TransformationStatus.COMPLETED:
            gLogger.info(
                f"[{trans_id}] Parent Transformation {parent_id} is not complete yet."
            )
            flush_trans = False

        if flush_trans:
            unused_trans_files = self.get_transformation_files(
                condDict={"TransformationID": trans_id, "Status": "Unused"}
            )
            if not unused_trans_files["OK"]:
                return unused_trans_files

            count_unused = len(unused_trans_files["Value"])
            if group_size > count_unused and count_unused != 0:
                res_flush = self.trans_client.setTransformationParameter(
                    trans_id, paramName="Status", paramValue=TransformationStatus.FLUSH
                )
                if res_flush["OK"]:
                    message = (
                        "Nb of files with Status 'Unused' "
                        f"({count_unused}) < GroupSize ({group_size})\n"
                        f"The Transformation {trans_id} has been Flushed"
                    )
                    self.send_mail(
                        subject=self.subject + f"Flush Transformation {trans_id}",
                        message=message,
                    )
                    return s_report(False, message)
                else:
                    return res_flush

    def parse_transformation_jobs_attributes(
        self, trans_id: int, jobs_attributes: list, create_report: bool = True
    ) -> Union[DOKReturnType[dict], Any, DErrorReturnType]:
        """Create a transformation report giving the number of jobs
        with a given application status by sites"""

        count_status_type: dict = {}
        count_minor_status: dict = {}
        count_status: dict = {}

        total_nb_jobs: int = len(jobs_attributes.keys())

        # Count jobs by status type:
        for job_id, job_info in jobs_attributes.items():
            job_info["TransID"] = str(trans_id)
            job_attributes_tuple = tuple(
                job_info[attr] for attr in self.attributes_of_interest
            )

            status_counts = count_status_type.get(job_attributes_tuple, 0)
            count_status_type[job_attributes_tuple] = status_counts + 1

            count_minor_status[job_info["MinorStatus"]] = (
                count_minor_status.get(job_info["MinorStatus"], 0) + 1
            )
            count_status[job_info["Status"]] = (
                count_status.get(job_info["Status"], 0) + 1
            )
        if not count_status_type:
            return S_ERROR(f"[{trans_id}] Empty Transformation")

        if create_report:
            htlm_job_report: str = self.create_transformation_jobs_report(
                trans_id,
                count_status_type,
                count_minor_status,
                count_status,
                total_nb_jobs,
            )
            return S_OK(htlm_job_report)
        else:
            return S_OK()

    def create_transformation_jobs_report(
        self,
        trans_id: int,
        count_status_type: dict,
        count_minor_status: dict,
        count_status: dict,
        total_nb_jobs: int,
    ) -> str:
        """Create the Rich transformation jobs report"""
        title: str = f"Transformation: {trans_id}"
        fields: list[str] = ["TransID"] + self.attributes_of_interest + ["Total"]
        table: Table = self.init_rich_table(title, fields)

        self.add_rows_in_table(
            count_minor_status,
            count_status,
            count_status_type,
            total_nb_jobs,
            trans_id,
            table,
        )

        return self.generate_table(table, self.html)

    def add_rows_in_table(
        self,
        count_minor_status: dict,
        count_status: dict,
        count_status_type: dict,
        total_nb_jobs: int,
        trans_id: int,
        table: Table,
    ) -> None:
        """Add rows in the table"""
        next_minor_status = ""
        next_status = ""
        # Sort the StatusType by Status then by MinorStatus:
        count_status_type_sorted: list = sorted(
            count_status_type, key=self.sorting_key(1, 2)
        )
        N: int = len(count_status_type_sorted)
        n = 0
        for status_tuple in count_status_type_sorted:
            row = (
                [f"{trans_id}"]
                + list(status_tuple)
                + [str(count_status_type[status_tuple])]
            )
            table.add_row(*row)
            # Add Total
            if n + 1 <= N:
                if n + 1 < N:
                    next_status, next_minor_status = self.get_next_status(
                        n, count_status_type_sorted
                    )
                # Add minor_status total
                if self.should_add_minor_status_total(
                    n, next_minor_status, status_tuple, N
                ):
                    row = self.minor_status_total_row(
                        row, count_minor_status, status_tuple, count_status
                    )
                    table.add_row(*row)
                # Add status total
                if self.should_add_status_total(n, next_status, status_tuple, N):
                    row = self.status_total_row(
                        row, count_status, status_tuple, total_nb_jobs
                    )
                    table.add_row(*row)
            n += 1
        final_row: list[str] = self.final_row(trans_id, total_nb_jobs)
        table.add_row(*final_row)

    def get_next_status(
        self, n: int, count_status_type_sorted: list
    ) -> tuple[Any, Any]:
        """Get the next job status"""
        next_status: str = (
            count_status_type_sorted[n + 1][0]
            if n + 1 < len(count_status_type_sorted)
            else ""
        )
        next_minor_status: str = (
            count_status_type_sorted[n + 1][1]
            if n + 1 < len(count_status_type_sorted)
            else ""
        )
        return next_status, next_minor_status

    def should_add_minor_status_total(
        self, n: int, next_minor_status: str, status_tuple: tuple, tot: int
    ) -> Union[Any, bool]:
        """Condition to add the total of minor status"""
        return (next_minor_status != status_tuple[1] and next_minor_status != "") or (
            n + 1 == tot
        )

    def minor_status_total_row(
        self,
        row: list,
        count_minor_status: dict,
        status_tuple: tuple,
        count_status: dict,
    ) -> list[str]:
        """Create the minor status total row"""
        row[2] = f"Total: {row[2]}"
        row[-1] = (
            f"{count_minor_status[status_tuple[1]]} "
            f"({round(count_minor_status[status_tuple[1]]/count_status[status_tuple[0]]*100, 1)}%)"
        )
        row[-2] = "-"
        row[3] = "-"
        return [f"[bold]{r}" for r in row]

    def should_add_status_total(
        self, n: int, next_status: str, status_tuple: tuple, tot: int
    ) -> Union[Any, bool, str]:
        """Condition on creating the total status"""
        return (next_status != status_tuple[0] and next_status) or (n + 1 == tot)

    def status_total_row(
        self, row: list, count_status: dict, status_tuple: tuple, total_nb_jobs: int
    ) -> list[str]:
        """Create the status total row"""
        row[1] = f"Total: {row[1]}"
        row[-1] = (
            f"{count_status[status_tuple[0]]} "
            f"({round(count_status[status_tuple[0]]/total_nb_jobs*100, 1)}%)"
        )
        row[2] = "-"

        if row[1] in ("Failed", "Killed"):
            color = "bold red"
        elif "Done" in row[1]:
            color = "bold green"
        else:
            color = "bold yellow"
        return [f"[{color}]{r}" for r in row]

    def final_row(self, trans_id: int, total_nb_jobs: int) -> list[str]:
        """Create the final row with total number of jobs"""
        final_row: list[str] = [
            f"Total: {trans_id}",
            "-",
            "-",
            "-",
            "-",
            str(total_nb_jobs),
        ]
        return [f"[bold]{f}" for f in final_row]

    def create_threads_for_each_transformations(self, transformations) -> dict:
        """Create the future threads to run check for each transformation"""
        future_to_trans_id: dict = {}
        for trans_id, trans_info_dict in transformations["Value"].items():
            trans_type = trans_info_dict["Type"]
            trans_id = int(trans_id)
            try:
                future = self.thread_pool_executor.submit(
                    self.check_transformation, trans_id, trans_info_dict
                )
                future_to_trans_id[future] = (trans_id, trans_type)
            except Exception.error as e:
                gLogger.info(e)
        return future_to_trans_id

    def beforeExecuting(self) -> None:
        self.get_cs_options()

    def execute(self) -> Union[DErrorReturnType, DOKReturnType[None]]:
        """Execution in one agent's cycle"""
        self.beforeExecuting()

        transformations = self.get_eligible_transformation(
            self.transformation_status, self.transformation_types
        )
        if not transformations["OK"]:
            gLogger.error("Failure to get transformations")
            return S_ERROR(transformations["Message"])

        future_to_trans_id = self.create_threads_for_each_transformations(
            transformations
        )

        # Get results:
        # TODO: Simplify the output parsing
        transformation_reports: dict[str, dict[str, str]] = defaultdict(dict)
        for future in concurrent.futures.as_completed(future_to_trans_id):
            trans_id, trans_type = future_to_trans_id[future]
            try:
                result = future.result()
                if result["OK"]:
                    trans_report = result["Value"]
                    if trans_report["Report"]:
                        transformation_reports[trans_type][trans_id] = trans_report[
                            "Message"
                        ]
                        gLogger.info(f"Report for transformation {trans_id} created")
                    else:
                        gLogger.info(trans_report["Message"])
                else:
                    gLogger.error(result)
            except Exception as exc:
                gLogger.error(f"{trans_id} generated an exception: {exc}")
                gLogger.debug(future.result())
            else:
                gLogger.info(f"Processed transformation {trans_id}")

        if transformation_reports:
            message: str = self.create_mail_message(
                transformation_reports, html=self.html
            )
            self.send_mail(
                subject=(
                    f"{self.subject} Report on "
                    f"{self.transformation_status} transformations"
                ),
                message=message,
                html=self.html,
            )
        return S_OK()

    def finalize(self) -> DOKReturnType[None]:
        """Final step of one cycle"""
        try:
            self.thread_pool_executor.shutdown()
        except Exception.error as e:
            gLogger.error(f"Threads shutdown failed: {e}")
        else:
            gLogger.info("Finishing threads")
        return S_OK()
