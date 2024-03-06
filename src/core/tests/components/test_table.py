import pytest
from workflows_engine.core.components import Input, Table, Button
from workflows_engine.exceptions import InvalidArguments
# from workflows_engine import validators

from ..schema_validator import get_validator_for


@pytest.fixture
def field():
    return Input(label="Input")

@pytest.fixture
def field2():
    return Input(label="Input 2")

def test_table(field, field2):
    """Test table component creates json matching json schema"""
    table = Table(
        table_components=[field, field, field2],
        table_data_path="$.table_data",
        table_headers_path="$.table_headers",
    )
    validator = get_validator_for("components/table")
    validator.validate(table.get_base_component_dict())
