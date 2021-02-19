import pytest
from workflows_engine.core.components import Modal, Button

from ..schema_validator import get_validator_for


def test_modal():
    """Test modal component creates json matching json schema"""
    modal = Modal(
        title="Modal Title",
        components=[Button(text="Button", action="submit", style="primary")],
    )
    validator = get_validator_for("components/modal")
    validator.validate(modal.get_base_component_dict())
