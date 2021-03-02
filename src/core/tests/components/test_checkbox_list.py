import pytest
from workflows_engine.core.components import CheckboxList
from workflows_engine.exceptions import InvalidArguments

from ..schema_validator import get_validator_for


def test_checkboxlist_data_path():
    """Test checkbox_list component creates json matching json schema"""
    checkboxlist = CheckboxList(
        title="CheckboxList Title",
        destination_path="$.result",
        data_path="$.checkboxlist_data_location",
    )
    validator = get_validator_for("components/checkbox_list")
    validator.validate(checkboxlist.get_base_component_dict())


def test_checkboxlist_data():
    """Test checkbox_list component creates json matching json schema"""
    checkboxlist = CheckboxList(
        title="CheckboxList Title",
        destination_path="$.result",
        data=[
            {
                "label": "Label of checkbox 1",
                "value": "Value 1",
            },
            {
                "label": "Label of checkbox 2",
                "value": "Value 2",
            },
        ],
    )
    validator = get_validator_for("components/checkbox_list")
    validator.validate(checkboxlist.get_base_component_dict())


def test_checkboxlist_missing_required_arg():
    """Test missing required argument correctly raises issue"""
    with pytest.raises(InvalidArguments):
        CheckboxList(
            title="CheckboxList Title",
            destination_path="$.result",
        )


def test_checkboxlist_mutually_exclusive_args():
    """Test including mutually exclusive args correctly raises issue"""
    with pytest.raises(InvalidArguments):
        CheckboxList(
            title="CheckboxList Title",
            destination_path="$.result",
            data_path="$.checkboxlist_data_location",
            data=[
                {
                    "label": "Label of checkbox 1",
                    "value": "Value 1",
                },
                {
                    "label": "Label of checkbox 2",
                    "value": "Value 2",
                },
            ],
        )
