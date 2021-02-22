from ..schema_validator import get_validator_for
from workflows_engine.core import tasks, containers
from workflows_engine import validators


def test_jsonrpc():
    task = tasks.JsonRpc(
        name="task",
        url="/endpoint/task/url",
        preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
        method="GET",
        payload_paths=[
            containers.PayloadPath(source_path="$.arg1", destination_path="$.arg1_result"),
            containers.PayloadPath(source_path="$.arg2", destination_path="$.arg2_result"),
        ],
        payload={"arg1_result": None, "arg2_result": None},
        response_path="$.response",
    )
    validator = get_validator_for("tasks/jsonrpc")
    validator.validate(task.as_dict())
