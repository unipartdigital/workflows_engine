from ..validator import get_validator_for
from workflows_engine.core import tasks, components
from workflows_engine import validators


def test_local_store():
    task = tasks.LocalStore(
        name="local_store",
        preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
        context_path="$.local_value",
        storage_key="store_key",
    )
    validator = get_validator_for("tasks/set_local_storage")
    validator.validate(task.as_dict())
