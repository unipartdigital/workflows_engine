from ..schema_validator import get_validator_for
from workflows_engine.core import tasks, components
from workflows_engine import validators


def test_update():
    task = tasks.Update(
        name="update",
        preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
        tasks=[
            {"key": "$.src", "result_key": "$.dest"},
            {"result": True, "result_key": "$.dest"},
            {"template": "This is the source: {$.src}", "result_key": "$.dest"},
        ],
    )
    validator = get_validator_for("tasks/update")
    validator.validate(task.as_dict())
