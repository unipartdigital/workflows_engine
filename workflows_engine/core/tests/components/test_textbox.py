import pytest
from workflows_engine.core.components import Textbox

from ..schema_validator import get_validator_for


def test_textbox():
    """Test textbox component creates json matching json schema"""
    textbox = Textbox(
        # type="textbox",
        content="**MD** formatted **string**",
        align="centre"
    )
    validator = get_validator_for("components/textbox")
    validator.validate(textbox.get_base_component_dict())

