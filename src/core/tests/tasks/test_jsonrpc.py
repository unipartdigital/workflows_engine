from ..schema_validator import get_validator_for
from workflows_engine.core import tasks, components
from workflows_engine import validators


def test_jsonrpc():
    task = tasks.JsonRpc(
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
    validator = get_validator_for("tasks/jsonrpc")
    validator.validate(task.as_dict())
