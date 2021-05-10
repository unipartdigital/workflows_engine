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

