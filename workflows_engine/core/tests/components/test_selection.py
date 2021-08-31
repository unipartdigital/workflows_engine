import pytest
from workflows_engine.core.components import Input, Selection
from workflows_engine.exceptions import InvalidArguments

from ..schema_validator import get_validator_for


def test_selection_options_key():
    """Test select component creates json matching json schema"""
    selection = Selection(
        label="Select Fresh",
        style="primary",
        destination_path="$.result",
        options_key="$.optionlocation",
    )
    validator = get_validator_for("components/selection")
    validator.validate(selection.get_base_component_dict())


def test_selection_options_values():
    """Test select component creates json matching json schema"""
    selection = Selection(
        label="Select Fresh",
        style="primary",
        destination_path="$.result",
        options_values=[
            {"label": "wubbalubba", "value": "dubdub"},
            {"label": "rickyticky", "value": "taffy"}
        ],
    )
    validator = get_validator_for("components/selection")
    validator.validate(selection.get_base_component_dict())


def test_repeat_missing_required_arg():
    """Test missing required argument correctly raises issue"""
    with pytest.raises(InvalidArguments):
        Selection(
            label="Select Fresh",
            style="primary",
            destination_path="$.result",
        )


def test_repeat_no_missing_mutually_exclusive_args():
    """Test including mutually exclusive args correctly raises issue"""
    with pytest.raises(InvalidArguments):
        Selection(
            label="Select Fresh",
            style="primary",
            destination_path="$.result",
            options_key="$.optionlocation",
            options_values=[{"label": "wubbalubba", "value": "dubdub"}]
        )
