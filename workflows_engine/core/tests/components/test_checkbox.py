import pytest
from workflows_engine.core.components import Checkbox
from workflows_engine.exceptions import InvalidArguments

from ..schema_validator import get_validator_for


def test_checkbox_value_path():
    """Test checkbox component creates json matching json schema"""
    checkbox = Checkbox(
        label="Checkbox Label",
        value_path="$.value",
        destination_path="$.result",
    )
    validator = get_validator_for("components/checkbox")
    validator.validate(checkbox.get_base_component_dict())


def test_checkbox_value_string():
    """Test checkbox component creates json matching json schema"""
    checkbox = Checkbox(
        label="Checkbox Label",
        value="Hello World",
        destination_path="$.result",
    )
    validator = get_validator_for("components/checkbox")
    validator.validate(checkbox.get_base_component_dict())


def test_checkbox_value_bool():
    """Test checkbox component creates json matching json schema"""
    checkbox = Checkbox(
        label="Checkbox Label",
        value=True,
        destination_path="$.result",
    )
    validator = get_validator_for("components/checkbox")
    validator.validate(checkbox.get_base_component_dict())


def test_checkbox_missing_required_arg():
    """Test missing required argument correctly raises issue"""
    with pytest.raises(InvalidArguments):
        Checkbox(
            label="Checkbox Label",
        )


def test_checkbox_mutually_exclusive_args():
    """Test including mutually exclusive args correctly raises issue"""
    with pytest.raises(InvalidArguments):
        Checkbox(
            label="Checkbox Label",
            destination_path="$.result",
            value_path="$.value",
            value="Hello World",
        )
