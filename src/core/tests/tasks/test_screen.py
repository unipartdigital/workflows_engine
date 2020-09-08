from ..schema_validator import get_validator_for
from workflows_engine.core import tasks, components
from workflows_engine import validators


def test_screen():
    task = tasks.Screen(
        name="condition",
        components=[
            components.Button(text="Submit", action="submit", style="primary"),
            components.Button(text="Next", action="next", style="secondary"),
        ],
        status_msg_template="The screen completed",
        show_status_msg=True,
    )
    validator = get_validator_for("tasks/screen")
    validator.validate(task.as_dict())
