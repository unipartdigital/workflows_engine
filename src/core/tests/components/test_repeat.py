import pytest
from workflows_engine.core.components import Input, Repeat
from workflows_engine.exceptions import InvalidArguments
from workflows_engine import validators

from ..schema_validator import get_validator_for as schema_validator


@pytest.fixture
def field():
    return Input(label="Input")


@pytest.fixture
def component_validator():
    return validators.is_equal(
        validator_value=["ExpectedValue1", "ExpectedValue2", "ExpectedValue3"]
    )


def test_repeat(field, component_validator):
    """Test repeat component creates json matching json schema"""
    repeat = Repeat(
        components=field,
        validators=component_validator,
        quantity=3,
        destination_path="$.result",
    )
    validator = schema_validator("components/repeat")
    validator.validate(repeat.get_base_component_dict())


def test_repeat_missing_required_arg(field):
    """Test missing required argument correctly raises issue"""
    with pytest.raises(InvalidArguments):
        Repeat(
            components=field,
            validators=component_validator,
            destination_path="$.result",
        )


def test_repeat_no_missing_mutually_exclusive_args(field):
    """Test including mutually exclusive args correctly raises issue"""
    with pytest.raises(InvalidArguments):
        Repeat(
            components=field,
            validators=component_validator,
            quantity=3,
            quantity_path="$.quantity",
            destination_path="$.result",
        )