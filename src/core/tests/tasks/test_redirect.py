from ..validator import get_validator_for
from workflows_engine.core import tasks, components
from workflows_engine import validators


def test_redirect():
    task = tasks.Redirect(
        name="redirect",
        preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
        url="url/to/go/to",
    )
    validator = get_validator_for("tasks/redirect")
    validator.validate(task.as_dict())
