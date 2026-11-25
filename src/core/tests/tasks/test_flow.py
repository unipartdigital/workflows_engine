import pytest
from workflows_engine.core.tasks import Flow
from workflows_engine import validators
from ..schema_validator import get_validator_for


@pytest.fixture
def flow():
    return Flow(name="main_flow")


def test_add_task_to_flow(flow):
    task = flow.add_task(
        task_type="jsonrpc",
        name="task",
        url="/endpoint/task/url",
        method="GET",
        payload_paths=[
            {"key": "$.arg1", "result_key": "$.arg1_result"},
            {"key": "$.arg2", "result_key": "$.arg2_result"},
        ],
        payload={"arg1_result": None, "arg2_result": None},
        response_path="$.response",
    )

    assert task in flow.tasks, "Tasks do not contain result of add_task"


def test_flow_to_dict(flow):
    task = flow.add_task(
        task_type="jsonrpc",
        name="task",
        url="/endpoint/task/url",
        preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
        method="GET",
        payload_paths=[
            {"key": "$.arg1", "result_key": "$.arg1_result"},
            {"key": "$.arg2", "result_key": "$.arg2_result"},
        ],
        payload={"arg1_result": None, "arg2_result": None},
        response_path="$.response",
    )
    validator = get_validator_for("tasks/flow")
    validator.validate(flow.as_dict())


RESULT_KEYS = [{"key": "$.product", "result_key": "$.product"}]


def test_sub_flow_config_keeps_result_keys_without_result(flow):
    sub_flow = flow.add_task(
        task_type="flow", name="sub_flow", result_keys=RESULT_KEYS, destination_path=False
    )

    assert sub_flow.as_dict()["config"] == {
        "result": {},
        "result_keys": RESULT_KEYS,
        "destination_path": False,
    }


def test_sub_flow_config_keeps_result_keys_without_destination_path(flow):
    sub_flow = flow.add_task(
        task_type="flow", name="sub_flow", result={"product": None}, result_keys=RESULT_KEYS
    )

    assert sub_flow.as_dict()["config"] == {
        "result": {"product": None},
        "result_keys": RESULT_KEYS,
        "destination_path": None,
    }


def test_sub_flow_config_is_empty_without_result_keys(flow):
    sub_flow = flow.add_task(
        task_type="flow", name="sub_flow", destination_path="$.sub_flow_results"
    )

    assert sub_flow.as_dict()["config"] == {}
