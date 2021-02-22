from ..schema_validator import get_validator_for
from workflows_engine.core import tasks, containers
from workflows_engine import validators


def test_update():
    task = tasks.Update(
        name="update",
        preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
        tasks=[
            containers.ContextUpdateInstruction(source_path="$.src", destination_path="$.dest"),
            containers.ContextUpdateInstruction(value=True, destination_path="$.dest"),
            containers.ContextUpdateInstruction(
                template="This is the source: {$.src}",
                destination_path="$.dest",
            ),
        ],
    )
    validator = get_validator_for("tasks/update")
    validator.validate(task.as_dict())
