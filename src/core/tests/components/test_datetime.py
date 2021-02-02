import pytest
from workflows_engine.core.components import DateTime
from workflows_engine.exceptions import InvalidArguments

from ..schema_validator import get_validator_for


def test_datetime_date():
    """Test datetime component creates json matching json schema"""
    datetime = DateTime(
        datetime_type="date",
        label="Datetime",
        destination_path="$.result",
    )
    validator = get_validator_for("components/datetime")
    validator.validate(datetime.get_base_component_dict())

def test_datetime_datetime():
    """Test datetime component creates json matching json schema"""
    datetime = DateTime(
        datetime_type="datetime",
        label="Datetime",
        destination_path="$.result",
    )
    validator = get_validator_for("components/datetime")
    validator.validate(datetime.get_base_component_dict())
