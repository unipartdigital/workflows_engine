from ..schema_validator import get_validator_for
from workflows_engine.core import tasks, components, containers
from workflows_engine import validators


def test_condition():
    task = tasks.Condition(
        name="condition",
        preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
        conditions=validators.is_equal(value_key="$.another_value", validator_value="b"),
        on_success=containers.TaskTarget(
            flow_path="Base",
            task_name="SuccessTask",
        ),
        success_message=containers.Message(
            template="You we're successful",
            message_type="success",
        ),
        on_failure=containers.TaskTarget(
            flow_path="Base",
            task_name="FailureTask",
        ),
        failure_message=containers.Message(
            template="Failure",
            message_type="error",
        ),
    )
    validator = get_validator_for("tasks/condition")
    validator.validate(task.as_dict())
