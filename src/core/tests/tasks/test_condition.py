from ..schema_validator import get_validator_for
from workflows_engine.core import tasks, components
from workflows_engine import validators


def test_condition():
    task = tasks.Condition(
        name="condition",
        conditions=validators.is_equal(value_key="$.value", validator_value="a"),
        on_success="SuccessTask",
        success_message=components.Message(
            template="You we're successful",
            message_type="success",
        ),
        on_failure="FailureTask",
        failure_message=components.Message(
            template="Failure",
            message_type="error",
        ),
    )
    validator = get_validator_for("tasks/condition")
    validator.validate(task.as_dict())
