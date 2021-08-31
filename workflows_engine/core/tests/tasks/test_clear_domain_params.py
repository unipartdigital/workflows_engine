from ..schema_validator import get_validator_for
from workflows_engine.core import tasks, components
from workflows_engine import validators


def test_clear_domain_params():
    task = tasks.ClearDomainParams(
        name="clear_domain_params",
        preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
    )
    validator = get_validator_for("tasks/clear_domain_params")
    validator.validate(task.as_dict())
