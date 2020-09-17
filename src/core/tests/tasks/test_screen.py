from ..schema_validator import get_validator_for
from workflows_engine.core import tasks, components
from workflows_engine import validators


def test_screen():
    task = tasks.Screen(
        name="screen",
        components=[
            components.Button(text="Submit", action="submit", style="primary"),
            components.Button(text="Next", action="next", style="secondary"),
        ],
        status_message_template="The screen completed",
        show_status_message=True,
    )
    validator = get_validator_for("tasks/screen")
    validator.validate(task.as_dict())
