from collections import defaultdict
from unittest.mock import MagicMock, patch
from rich.table import Table
from CTADIRAC.Core.Utilities.return_values import s_report
from CTADIRAC.TransformationSystem.Agent.TransformationFailoverAgent import (
    TransformationFailoverAgent,
)


@patch("CTADIRAC.TransformationSystem.Agent.TransformationFailoverAgent.AgentModule")
@patch("CTADIRAC.TransformationSystem.Agent.TransformationFailoverAgent.JobDB")
@patch(
    "CTADIRAC.TransformationSystem.Agent.TransformationFailoverAgent.TransformationDB"
)
@patch.object(TransformationFailoverAgent, "get_cs_options")
def init_tfa(
    mock_am, mock_job_db, mock_trans_db, mock_cs_option
) -> TransformationFailoverAgent:
    mock_cs_option.return_value = None
    tfa = TransformationFailoverAgent()

    tfa.trans_db = mock_job_db
    tfa.job_db = mock_trans_db
    return tfa


def test_should_complete_transformation() -> None:
    tfa: TransformationFailoverAgent = init_tfa()
    tfa.get_parent_type = MagicMock(return_value=None)
    tfa.transformations_to_complete = ["Processing", "Merging"]
    trans_id = 2
    is_processed_return_values: list[bool] = [True, True]

    trans_type = "MCSimulation"
    parent_id = -1
    with patch.object(
        tfa, "is_transformation_processed", side_effect=is_processed_return_values
    ):
        result = tfa.should_complete_transformation(trans_type, trans_id, parent_id)
        assert result is False

    trans_type = "Processing"
    parent_id = 1
    tfa.get_parent_type = MagicMock(return_value=["MCSimulation"])
    with patch.object(
        tfa, "is_transformation_processed", side_effect=is_processed_return_values
    ):
        result = tfa.should_complete_transformation(trans_type, trans_id, parent_id)
        assert result is True

    trans_type = "Merging"
    parent_id = 1
    tfa.get_parent_type = MagicMock(return_value=["Processing"])
    with patch.object(
        tfa, "is_transformation_processed", side_effect=is_processed_return_values
    ):
        result = tfa.should_complete_transformation(trans_type, trans_id, parent_id)
        assert result is True

    is_processed_return_values: list[bool] = [False, True]
    trans_type = "Processing"
    parent_id = 1
    tfa.get_parent_type = MagicMock(return_value=["MCSimulation"])
    with patch.object(
        tfa, "is_transformation_processed", side_effect=is_processed_return_values
    ):
        result = tfa.should_complete_transformation(trans_type, trans_id, parent_id)
        assert result is False


def test_update_tasks_status() -> None:
    tfa: TransformationFailoverAgent = init_tfa()

    jobs_attributes = {1: {"Status": "Failed"}, 2: {"Status": "Done"}}
    tasks_infos = [
        {
            "ExternalID": 1,
            "ExternalStatus": "Failed",
            "TransformationID": 123,
            "TaskID": 1,
        },
        {
            "ExternalID": 2,
            "ExternalStatus": "Done",
            "TransformationID": 456,
            "TaskID": 2,
        },
    ]

    tfa.update_tasks_status(jobs_attributes, tasks_infos)
    # Verify that the tasks status are not changed:
    assert tfa.trans_db.setTaskStatus.call_count == 0

    tasks_infos = [
        {
            "ExternalID": 1,
            "ExternalStatus": "Submitting",
            "TransformationID": 123,
            "TaskID": 1,
        },
        {
            "ExternalID": 2,
            "ExternalStatus": "Completed",
            "TransformationID": 456,
            "TaskID": 2,
        },
    ]

    tfa.update_tasks_status(jobs_attributes, tasks_infos)
    # Verify that the tasks status are updated twice
    assert tfa.trans_db.setTaskStatus.call_count == 2


lfn_1 = "/path/to/file1.txt"
lfn_2 = "/path/to/file2.txt"


def test_get_lfns_to_assign() -> None:
    tfa: TransformationFailoverAgent = init_tfa()
    # Mock the get_transformation_files method
    tfa.get_transformation_files = MagicMock(
        return_value={
            "OK": True,
            "Value": [{"TaskID": 1, "LFN": lfn_1}, {"TaskID": 2, "LFN": lfn_2}],
        }
    )

    # Mock the update_reassign_count method
    tfa.update_reassign_count = MagicMock()

    # Define some sample data
    trans_id = 123
    failed_tasks = [1, 2]

    # Call the method being tested
    lfns_to_assign = tfa.get_lfns_to_assign(trans_id, failed_tasks)

    # Assert that the method returned the expected value
    assert lfns_to_assign == {1: lfn_1, 2: lfn_2}

    # Assert that get_transformation_files was called with the correct arguments
    tfa.get_transformation_files.assert_called_with(condDict={"TaskID": failed_tasks})

    # Assert that update_reassign_count was called for each LFN
    assert tfa.update_reassign_count.call_count == 2


def test_reassign_lfn() -> None:
    tfa: TransformationFailoverAgent = init_tfa()

    # Mock the get_tasks_by_file_status method
    tfa.trans_client.get_tasks_by_file_status = MagicMock(
        return_value={"OK": True, "Value": []}
    )

    # Mock the get_lfns_to_assign method
    tfa.get_lfns_to_assign = MagicMock(return_value={})

    # Mock the setFileStatusForTransformation method
    tfa.trans_client.setFileStatusForTransformation = MagicMock(
        return_value={"OK": True}
    )

    # Define some sample data
    trans_id = 123

    # Call the method being tested
    lfns_to_assign = tfa.reassign_lfn(trans_id)

    # Assert there is noo lfns to assign
    assert lfns_to_assign == {}

    # Assert setFileStatus is not called
    assert tfa.trans_client.setFileStatusForTransformation.call_count == 0

    tfa.trans_client.get_tasks_by_file_status = MagicMock(
        return_value={"OK": True, "Value": [1, 2]}
    )
    tfa.get_lfns_to_assign = MagicMock(return_value={1: lfn_1, 2: lfn_2})
    lfns_to_assign = tfa.reassign_lfn(trans_id)

    # Assert that the method returned the expected dictionary of LFNS
    assert lfns_to_assign == {1: lfn_1, 2: lfn_2}

    # Assert that get_tasks_by_file_status was called with the correct arguments
    tfa.trans_client.get_tasks_by_file_status.assert_called_with(
        trans_id, tfa.file_status_to_check, tfa.failed_final_task_status
    )

    # Assert that get_lfns_to_assign was called with the correct arguments
    tfa.get_lfns_to_assign.assert_called_with(trans_id, [1, 2])

    # Assert that setFileStatusForTransformation was called with the correct arguments
    tfa.trans_client.setFileStatusForTransformation.assert_called_with(
        trans_id, newLFNsStatus="Unused", lfns=[lfn_1, lfn_2], force=True
    )


def test_flush_transformation() -> None:
    tfa: TransformationFailoverAgent = init_tfa()

    # Mock getTransformation:
    tfa.trans_client.getTransformation = MagicMock(
        return_value={"OK": True, "Value": {"Status": "Active"}}
    )

    # Mock get_transformation_files:
    tfa.get_transformation_files = MagicMock(return_value={"OK": True, "Value": []})

    # Mock setTransformationParameter:
    tfa.trans_client.setTransformationParameter = MagicMock(return_value={"OK": True})

    # Mock send_mail
    tfa.send_mail = MagicMock(return_value=None)

    trans_id = 2
    trans_info_dict = {"GroupSize": 10}
    parent_id = 1
    tfa.flush_transformation(trans_id, trans_info_dict, parent_id)

    # Assert that methods are not called since transformation shoudll not be flushed
    assert tfa.get_transformation_files.call_count == 0
    assert tfa.trans_client.setTransformationParameter.call_count == 0

    tfa.trans_client.getTransformation = MagicMock(
        return_value={"OK": True, "Value": {"Status": "Completed"}}
    )
    parent_id = -1
    # Allow to flush trans but don't since there is no unused files
    tfa.get_transformation_files = MagicMock(return_value={"OK": True, "Value": []})
    tfa.flush_transformation(trans_id, trans_info_dict, parent_id)

    # assert get_trans_files is called once
    assert tfa.get_transformation_files.call_count == 1
    # Assert it is still called
    assert tfa.trans_client.setTransformationParameter.call_count == 0

    # Unused files found
    tfa.get_transformation_files = MagicMock(
        return_value={"OK": True, "Value": [lfn_1, lfn_2]}
    )
    result = tfa.flush_transformation(trans_id, trans_info_dict, parent_id)

    # assert get_trans_files is called once
    assert tfa.get_transformation_files.call_count == 1
    # Assert it is still called
    assert tfa.trans_client.setTransformationParameter.call_count == 1

    # Assert the message is return
    assert f"{trans_id} has been Flushed" in result["Value"]["Message"]


def test_parse_transformation_jobs_attributes() -> None:
    tfa: TransformationFailoverAgent = init_tfa()

    trans_id = 1
    jobs_attributes = {}

    result = tfa.parse_transformation_jobs_attributes(trans_id, jobs_attributes)
    # Assert there is an error message
    assert isinstance(result["Message"], str)

    jobs_attributes = {
        1: {
            "Status": "Done",
            "MinorStatus": "minorStatus1",
            "ApplicationStatus": "appStatus1",
            "Site": "Site1",
        },
        2: {
            "Status": "Done",
            "MinorStatus": "minorStatus2",
            "ApplicationStatus": "appStatus2",
            "Site": "Site2",
        },
    }

    result = tfa.parse_transformation_jobs_attributes(trans_id, jobs_attributes)
    # Assert there is a report
    assert isinstance(result["Value"], str)


def test_create_transformation_jobs_report() -> None:
    tfa: TransformationFailoverAgent = init_tfa()

    trans_id = 123
    attributes_of_interest = ["Status", "MinorStatus", "ApplicationStatus", "Site"]
    count_status_type = {
        ("Done", "minorStatus1", "appStatus1", "Site1"): 2,
        ("Done", "minorStatus2", "appStatus2", "Site2"): 3,
    }
    count_minor_status = {"minorStatus1": 2, "minorStatus2": 3}
    count_status = {"Done": 5}
    total_nb_jobs = 5

    # Call the method being tested
    report = tfa.create_transformation_jobs_report(
        trans_id,
        attributes_of_interest,
        count_status_type,
        count_minor_status,
        count_status,
        total_nb_jobs,
    )

    # Assert that the report is generated correctly
    assert isinstance(report, str)
    assert "Transformation: 123" in report


def test_add_rows_in_table():
    tfa: TransformationFailoverAgent = init_tfa()
    # Define mock input parameters
    count_minor_status = {"minorStatus1": 2, "minorStatus2": 3}
    count_status = {"Done": 5}
    count_status_type = {
        ("Done", "minorStatus1", "appStatus1", "Site1"): 2,
        ("Done", "minorStatus2", "appStatus2", "Site2"): 3,
    }
    total_nb_jobs = 5
    trans_id = 123
    table = Table()

    # Call the method being tested
    tfa.add_rows_in_table(
        count_minor_status,
        count_status,
        count_status_type,
        total_nb_jobs,
        trans_id,
        table,
    )

    assert table.row_count == 6


def test_get_next_status() -> None:
    tfa: TransformationFailoverAgent = init_tfa()

    # Test case 1: n < len(count_status_type_sorted)
    n = 0
    count_status_type_sorted = [
        ("Status1", "MinorStatus1"),
        ("Status2", "MinorStatus2"),
    ]
    expected_next_status = "Status2"
    expected_next_minor_status = "MinorStatus2"
    next_status, next_minor_status = tfa.get_next_status(n, count_status_type_sorted)
    assert next_status == expected_next_status
    assert next_minor_status == expected_next_minor_status

    # Test case 2: n == len(count_status_type_sorted)
    n = 1
    count_status_type_sorted = [
        ("Status1", "MinorStatus1"),
        ("Status2", "MinorStatus2"),
    ]
    expected_next_status = ""
    expected_next_minor_status = ""
    next_status, next_minor_status = tfa.get_next_status(n, count_status_type_sorted)
    assert next_status == expected_next_status
    assert next_minor_status == expected_next_minor_status


def test_create_threads_for_each_transformations():
    # Mock data
    transformations = {
        "Value": {
            "1": {"Type": "Type1"},
            "2": {"Type": "Type2"},
        }
    }

    # Mock the ThreadPoolExecutor object
    mock_thread_pool_executor = MagicMock()

    # Mock the submit method of the executor instance
    mock_future_1 = MagicMock()
    mock_future_2 = MagicMock()
    mock_thread_pool_executor.submit.side_effect = [mock_future_1, mock_future_2]

    # Create an instance of YourClass
    tfa: TransformationFailoverAgent = init_tfa()
    tfa.thread_pool_executor = mock_thread_pool_executor
    # Call the method to be tested
    future_to_trans_id = tfa.create_threads_for_each_transformations(transformations)

    # Assertions
    assert isinstance(future_to_trans_id, dict)
    assert (
        len(future_to_trans_id) == 2
    )  # Check if both futures are added to the dictionary
    assert mock_future_1 in future_to_trans_id
    assert mock_future_2 in future_to_trans_id
    assert future_to_trans_id[mock_future_1] == (
        1,
        "Type1",
    )  # Check the values associated with the future
    assert future_to_trans_id[mock_future_2] == (
        2,
        "Type2",
    )  # Check the values associated with the future


def test_check_transformation() -> None:
    trans_id = 123
    trans_info_dict = {"Type": "Active"}
    tfa: TransformationFailoverAgent = init_tfa()

    # Define mock return values for methods called within check_transformation
    tfa.get_parent_transformation_id = MagicMock(return_value=-1)
    tfa.get_transformation_tasks = MagicMock(
        return_value={"Value": [{"ExternalID": "1"}, {"ExternalID": "2"}]}
    )
    tfa.update_tasks_status = MagicMock()
    tfa.should_complete_transformation = MagicMock(return_value=False)
    tfa.transformation_to_flush = []
    tfa.transformation_to_reschedule = []
    tfa.transformation_to_report = ["Active"]
    tfa.reassign_lfn = MagicMock(return_value={})
    tfa.create_reassigned_lfn_report = MagicMock(return_value="Report")

    excpted_return = {"OK": True, "Value": "Report"}
    tfa.parse_transformation_jobs_attributes = MagicMock(return_value=excpted_return)

    expected_result = s_report(True, excpted_return["Value"])
    result = tfa.check_transformation(trans_id, trans_info_dict)
    assert result == expected_result


@patch("concurrent.futures")
def test_execute(mock_concurrent_futures):
    tfa: TransformationFailoverAgent = init_tfa()
    tfa.transformation_status = "Active"
    tfa.transformation_types = ["Type1, Type2"]
    tfa.beforeExecuting = MagicMock()
    tfa.get_eligible_transformation = MagicMock(
        return_value={
            "OK": True,
            "Value": {"trans_id1": {"Type": "Type1"}, "trans_id2": {"Type": "Type2"}},
        }
    )

    # Mock future result
    mock_future1 = MagicMock()
    mock_future2 = MagicMock()
    excpeted_return_1 = {"OK": True, "Value": "Report1"}
    excpeted_return_2 = {"OK": True, "Value": "Report2"}
    mock_future1.result.return_value = s_report(True, excpeted_return_1["Value"])
    mock_future2.result.return_value = s_report(True, excpeted_return_2["Value"])
    expected_future_result = {
        mock_future1: ("trans_id1", "Type1"),
        mock_future2: ("trans_id2", "Type2"),
    }
    tfa.create_threads_for_each_transformations = MagicMock(
        return_value=expected_future_result
    )
    mock_concurrent_futures.as_completed.return_value = [mock_future1, mock_future2]

    tfa.create_mail_message = MagicMock()
    tfa.send_mail = MagicMock()

    # Call the method being tested
    result = tfa.execute()

    expected_trans_report_result = defaultdict(dict)
    expected_trans_report_result["Type1"] = {"trans_id1": "Report1"}
    expected_trans_report_result["Type2"] = {"trans_id2": "Report2"}
    tfa.create_mail_message.assert_called_once_with(expected_trans_report_result)

    expected_result = {"OK": True, "Value": None}
    assert result == expected_result
