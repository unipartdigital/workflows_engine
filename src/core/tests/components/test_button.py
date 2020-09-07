from workflows_engine.core.components import Button

from ..validator import get_validator_for


def test_button():
    button = Button(text="Button", action="submit", style="primary")
    validator = get_validator_for("components/button")
    validator.validate(button.get_base_component_dict())
