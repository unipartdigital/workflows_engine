from ..validator import get_validator_for
from workflows_engine.core import tasks, components
from workflows_engine import validators


def test_event():
    task = tasks.Event(
        name="event",
        preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
        action="break",
        payload={"X": "Y"},
    )
    validator = get_validator_for("tasks/event")
    validator.validate(task.as_dict())
