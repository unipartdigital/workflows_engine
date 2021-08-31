from ..schema_validator import get_validator_for
from workflows_engine.core import tasks, components
from workflows_engine import validators


def test_set_domain_param():
    task = tasks.DomainParam(
        name="set_domain_param",
        preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
        context_path="$.context_value",
        param="parameter",
    )
    validator = get_validator_for("tasks/set_domain_param")
    validator.validate(task.as_dict())
