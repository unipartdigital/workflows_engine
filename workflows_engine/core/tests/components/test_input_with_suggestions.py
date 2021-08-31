import pytest
from workflows_engine.core.components import InputWithSuggestions
from workflows_engine.exceptions import InvalidArguments

from ..schema_validator import get_validator_for


def test_input_with_suggestions_data_path():
    """Test input_with_suggestions component creates json matching json schema"""
    input_with_suggestions = InputWithSuggestions(
        label="Input With Suggestions",
        suggestions_path="$.input_with_suggestions_data_location",
    )
    validator = get_validator_for("components/input_with_suggestions")
    validator.validate(input_with_suggestions.get_base_component_dict())


def test_input_with_suggestions_data():
    """Test input_with_suggestions component creates json matching json schema"""
    input_with_suggestions = InputWithSuggestions(
        label="Input With Suggestions",
        suggestions=[
            {"name": "Suggestion 1"},
            {"name": "Suggestion 2"},
        ]
    )
    validator = get_validator_for("components/input_with_suggestions")
    validator.validate(input_with_suggestions.get_base_component_dict())


def test_input_with_suggestions_missing_required_arg():
    """Test missing required argument correctly raises issue"""
    with pytest.raises(InvalidArguments):
        InputWithSuggestions(
            label="Input With Suggestions",
        )


def test_input_with_suggestions_mutually_exclusive_args():
    """Test including mutually exclusive args correctly raises issue"""
    with pytest.raises(InvalidArguments):
        InputWithSuggestions(
            label="Input With Suggestions",
            suggestions_path="$.input_with_suggestions_data_location",
            suggestions=[
                {"name": "Suggestion 1"},
                {"name": "Suggestion 2"},
            ],
        )
