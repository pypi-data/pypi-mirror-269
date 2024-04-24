import datetime
from unittest.mock import patch
from rich.table import Table

from CTADIRAC.TransformationSystem.Utils.FailoverUtilities import FailoverUtilities

AGENT_NAME = "Transformation/TransformationFailoverAgent"

failover_utils = FailoverUtilities(AGENT_NAME)
# Defining TransformationClient Mock
with patch(
    "DIRAC.TransformationSystem.Client.TransformationClient.TransformationClient"
) as mock_transformation_client:
    failover_utils.trans_client = mock_transformation_client

with patch(
    "DIRAC.ProductionSystem.Client.ProductionClient.ProductionClient"
) as mock_production_client:
    failover_utils.prod_client = mock_production_client

with patch(
    "DIRAC.FrameworkSystem.Client.NotificationClient.NotificationClient"
) as mock_notification_client:
    failover_utils.notif_client = mock_notification_client

get_transformation_return_result = {
    "OK": True,
    "Value": [
        {
            "TransformationID": 448,
            "TransformationName": "00000122_Step1_MCSimulation",
            "Description": "description",
            "LongDescription": "longDescription",
            "CreationDate": datetime.datetime(2024, 1, 18, 8, 51, 41),
            "LastUpdate": datetime.datetime(2024, 1, 18, 8, 51, 43),
            "AuthorDN": "/DC=org/DC=terena/DC=tcs/C=DE/ST=Hamburg/O=Deutsches Elektronen-Synchrotron DESY/CN=majestix-vm1.zeuthen.desy.de",
            "AuthorGroup": "hosts",
            "Type": "MCSimulation",
            "Plugin": "Standard",
            "AgentType": "Automatic",
            "Status": "Active",
            "FileMask": "",
            "TransformationGroup": "General",
            "GroupSize": 1.0,
            "InheritedFrom": 0,
            "Body": "<Workflow></Workflow>\n",
            "MaxNumberOfTasks": 0,
            "EventsPerTask": 0,
            "TransformationFamily": "0",
        }
    ],
}


def test_get_eligible_transformation() -> None:
    failover_utils.trans_client.getTransformations.return_value = (
        get_transformation_return_result
    )

    result = failover_utils.get_eligible_transformation("Active", "MCSimulation")
    assert result["OK"] is True
    assert list(result["Value"].keys()) == ["448"]
    assert result["Value"]["448"] == get_transformation_return_result["Value"][0]


get_transformation_tasks_result = {
    "OK": True,
    "Value": [
        {
            "TaskID": 1,
            "TransformationID": 448,
            "ExternalStatus": "Done",
            "ExternalID": "50299",
            "TargetSE": "Unknown",
            "CreationTime": datetime.datetime(2024, 1, 18, 8, 51, 44),
            "LastUpdateTime": datetime.datetime(2024, 1, 18, 9, 4, 16),
        },
        {
            "TaskID": 2,
            "TransformationID": 448,
            "ExternalStatus": "Done",
            "ExternalID": "50303",
            "TargetSE": "Unknown",
            "CreationTime": datetime.datetime(2024, 1, 18, 8, 51, 44),
            "LastUpdateTime": datetime.datetime(2024, 1, 18, 9, 16, 15),
        },
        {
            "TaskID": 3,
            "TransformationID": 448,
            "ExternalStatus": "Done",
            "ExternalID": "50306",
            "TargetSE": "Unknown",
            "CreationTime": datetime.datetime(2024, 1, 18, 8, 51, 44),
            "LastUpdateTime": datetime.datetime(2024, 1, 18, 9, 4, 16),
        },
        {
            "TaskID": 4,
            "TransformationID": 448,
            "ExternalStatus": "Done",
            "ExternalID": "50309",
            "TargetSE": "Unknown",
            "CreationTime": datetime.datetime(2024, 1, 18, 8, 51, 44),
            "LastUpdateTime": datetime.datetime(2024, 1, 18, 9, 16, 15),
        },
        {
            "TaskID": 5,
            "TransformationID": 448,
            "ExternalStatus": "Done",
            "ExternalID": "50312",
            "TargetSE": "Unknown",
            "CreationTime": datetime.datetime(2024, 1, 18, 8, 51, 44),
            "LastUpdateTime": datetime.datetime(2024, 1, 18, 9, 4, 16),
        },
        {
            "TaskID": 6,
            "TransformationID": 448,
            "ExternalStatus": "Done",
            "ExternalID": "50315",
            "TargetSE": "Unknown",
            "CreationTime": datetime.datetime(2024, 1, 18, 8, 51, 44),
            "LastUpdateTime": datetime.datetime(2024, 1, 18, 9, 4, 16),
        },
        {
            "TaskID": 7,
            "TransformationID": 448,
            "ExternalStatus": "Done",
            "ExternalID": "50318",
            "TargetSE": "Unknown",
            "CreationTime": datetime.datetime(2024, 1, 18, 8, 51, 44),
            "LastUpdateTime": datetime.datetime(2024, 1, 18, 9, 4, 16),
        },
        {
            "TaskID": 8,
            "TransformationID": 448,
            "ExternalStatus": "Done",
            "ExternalID": "50321",
            "TargetSE": "Unknown",
            "CreationTime": datetime.datetime(2024, 1, 18, 8, 51, 44),
            "LastUpdateTime": datetime.datetime(2024, 1, 18, 9, 4, 16),
        },
        {
            "TaskID": 9,
            "TransformationID": 448,
            "ExternalStatus": "Done",
            "ExternalID": "50324",
            "TargetSE": "Unknown",
            "CreationTime": datetime.datetime(2024, 1, 18, 8, 51, 44),
            "LastUpdateTime": datetime.datetime(2024, 1, 18, 9, 4, 16),
        },
        {
            "TaskID": 10,
            "TransformationID": 448,
            "ExternalStatus": "Done",
            "ExternalID": "50302",
            "TargetSE": "Unknown",
            "CreationTime": datetime.datetime(2024, 1, 18, 8, 51, 44),
            "LastUpdateTime": datetime.datetime(2024, 1, 18, 9, 4, 16),
        },
    ],
}


def test_get_transformation_tasks() -> None:
    failover_utils.trans_client.getTransformationTasks.return_value = (
        get_transformation_tasks_result
    )

    result = failover_utils.get_transformation_tasks(448)
    assert result["OK"] is True
    assert result["Value"] == get_transformation_tasks_result["Value"]

    failover_utils.trans_client.getTransformationTasks.return_value = {
        "OK": False,
        "Value": [],
        "Message": "ERROR",
    }
    result = failover_utils.get_transformation_tasks(0)
    assert result["Message"] == "ERROR"


get_transformation_files_result = {
    "OK": True,
    "Value": [
        {
            "LFN": "/vo.cta.in2p3.fr/tests/prodsys/MC/Prod5bTest/LaPalma/gamma-diffuse/sim_telarray/448/Data/000xxx/gamma_20deg_0deg_run8___cta-prod5b-lapalma_desert-2158m-LaPalma-dark_cone10.simtel.zst",
            "TransformationID": 449,
            "FileID": 2742,
            "Status": "Processed",
            "TaskID": 3,
            "TargetSE": "Unknown",
            "UsedSE": "PIC-Disk",
            "ErrorCount": 0,
            "LastUpdate": datetime.datetime(2024, 1, 18, 9, 2, 58),
            "InsertedTime": datetime.datetime(2024, 1, 18, 9, 0, 2),
        }
    ],
}


def test_get_transformation_files() -> None:
    failover_utils.trans_client.getTransformationFiles.return_value = (
        get_transformation_files_result
    )

    result = failover_utils.get_transformation_files({"TransformationID": 449})
    assert result == get_transformation_files_result["Value"]


get_transformation_stats_result = {
    "OK": True,
    "Value": {"Processed": 10, "Total": 10},
    "rpcStub": (
        (
            "Transformation/TransformationManager",
            {"timeout": 600, "useAccessToken": False},
        ),
        "getTransformationStats",
        [449],
    ),
}


def test_is_transformation_processed() -> None:
    failover_utils.trans_client.getTransformationStats.return_value = (
        get_transformation_stats_result
    )

    result = failover_utils.is_transformation_processed(449)
    assert result is True

    failover_utils.trans_client.getTransformationStats.return_value = {
        "OK": True,
        "Value": {"Processed": 6, "Total": 10},
    }

    result = failover_utils.is_transformation_processed(449)
    assert result is False

    failover_utils.trans_client.getTransformationStats.return_value = {
        "OK": False,
        "Value": [],
    }
    result = failover_utils.is_transformation_processed(449)
    assert result is False


complete_transformation_result = {
    "OK": True,
    "Value": 0,
    "rpcStub": (
        (
            "Transformation/TransformationManager",
            {"timeout": 600, "useAccessToken": False},
        ),
        "setTransformationParameter",
        [466, "Status", "Completed"],
    ),
}


def test_complete_transformation() -> None:
    failover_utils.trans_client.completeTransformation.return_value = (
        complete_transformation_result
    )

    result = failover_utils.complete_transformation(466)
    assert result["Value"]["Message"] == "[466] Transformation Completed."

    failover_utils.trans_client.completeTransformation.return_value = {
        "OK": False,
        "Value": None,
    }
    result = failover_utils.complete_transformation(466)
    assert "[466]: Can't complete transformation" in result["Message"]


def test_get_parent_transformation_id() -> None:
    failover_utils.prod_client.get_parent_transformation.return_value = {
        "OK": True,
        "Value": [[-1]],
    }
    result = failover_utils.get_parent_transformation_id(466)
    assert result == -1

    failover_utils.prod_client.get_parent_transformation.return_value = {
        "OK": True,
        "Value": [],
    }
    result = failover_utils.get_parent_transformation_id(466)
    assert result is None

    failover_utils.prod_client.get_parent_transformation.return_value = {
        "OK": False,
        "Value": [],
    }
    result = failover_utils.get_parent_transformation_id(466)
    assert result is None


def test_get_parent_type() -> None:
    parent_id = 123
    mock_response = {"OK": True, "Value": [{"Type": "MockParentType"}]}

    failover_utils.trans_client.getTransformations.return_value = mock_response
    parent_type = failover_utils.get_parent_type(parent_id)

    assert parent_type == "MockParentType"


def test_sorting_key() -> None:
    sample_data = [("b", 2, "foo"), ("a", 3, "bar"), ("c", 1, "baz")]

    expected_sorted_result = [("a", 3, "bar"), ("b", 2, "foo"), ("c", 1, "baz")]

    sorted_data = sorted(sample_data, key=failover_utils.sorting_key(0, 1))

    assert sorted_data == expected_sorted_result


def test_create_mail_message() -> None:
    trans_type = "Processing"
    trans_id = 466
    trans_report: dict[str, dict[str, str]] = {trans_type: {f"{trans_id}": "Message"}}
    result: str = failover_utils.create_mail_message(trans_report)
    assert isinstance(result, str)
    for line in result.split("\n"):
        if '<span class="r1">' in line:
            report_header: str = line.split('<span class="r1">')[1].split("<")[0]
            assert report_header == "Report on Processing transformations:"


def test_init_rich_table() -> None:
    result: Table = failover_utils.init_rich_table("Test", ["f1", "f2"])
    assert isinstance(result, Table)


def test_generate_html_table() -> None:
    table: Table = failover_utils.init_rich_table("Test", ["f1", "f2"])
    result: str = failover_utils.generate_html_table(table)
    header: str = result.split("\n")[0]
    foot: str = result.split("\n")[-2]
    assert header == "<!DOCTYPE html>"
    assert foot == "</html>"


def test_send_mail() -> None:
    failover_utils.notif_client.sendMail.return_value = {"OK": True, "Value": "Message"}
    failover_utils.send_mail("Subject", "Message")
