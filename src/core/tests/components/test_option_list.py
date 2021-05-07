import pytest
from workflows_engine.core.components import OptionList
from workflows_engine.exceptions import InvalidArguments

from ..schema_validator import get_validator_for


def test_optionlist_data_path():
    """Test optionlist component creates json matching json schema"""
    optionlist = OptionList(
        title="OptionList Title",
        destination_path="$.result",
        display_type="details",
        data="**label1:** value1\n**label1:**value1\n"
    )
    validator = get_validator_for("components/option_list")
    validator.validate(optionlist.get_base_component_dict())


# def test_optionlist_missing_required_arg():
#     """Test missing required argument correctly raises issue"""
#     with pytest.raises(InvalidArguments):
#         OptionList(
#             title="OptionList Title",
#             destination_path="$.result",
#             display_type="details",
#         )


# def test_checkboxlist_mutually_exclusive_args():
#     """Test including mutually exclusive args correctly raises issue"""
#     with pytest.raises(InvalidArguments):
#         CheckboxList(
#             title="CheckboxList Title",
#             destination_path="$.result",
#             data_path="$.checkboxlist_data_location",
#             data=[
#                 {
#                     "label": "Label of checkbox 1",
#                     "value": "Value 1",
#                 },
#                 {
#                     "label": "Label of checkbox 2",
#                     "value": "Value 2",
#                 },
#             ],
#         )