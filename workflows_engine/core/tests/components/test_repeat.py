import pytest
from workflows_engine.core.components import Input, Repeat
from workflows_engine.exceptions import InvalidArguments
from workflows_engine import validators

from ..schema_validator import get_validator_for


@pytest.fixture
def field():
    return Input(label="Input")


def test_repeat(field):
    """Test repeat component creates json matching json schema"""
    repeat = Repeat(
        components=[field],
        times_to_repeat=3,
        destination_path="$.result",
    )
    validator = get_validator_for("components/repeat")
    validator.validate(repeat.get_base_component_dict())


def test_repeat_missing_required_arg(field):
    """Test missing required argument correctly raises issue"""
    with pytest.raises(InvalidArguments):
        Repeat(
            components=field,
            destination_path="$.result",
        )


def test_repeat_no_missing_mutually_exclusive_args(field):
    """Test including mutually exclusive args correctly raises issue"""
    with pytest.raises(InvalidArguments):
        Repeat(
            components=field,
            times_to_repeat=3,
            times_to_repeat_path="$.quantity",
            destination_path="$.result",
        )
