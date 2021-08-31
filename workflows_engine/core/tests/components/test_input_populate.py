import pytest
from ..schema_validator import get_validator_for
from workflows_engine.exceptions import InvalidArguments
from workflows_engine.validators.basic import greater_than_zero
from workflows_engine.core.containers import Populate


def test_populate_path():
    """ Test populate class with optionals path parameters """
    populate = Populate(
        validators=[greater_than_zero()],
        path="$.pick_details.quants[?(@.product.barcode == 'product')].qty",
    )
    validator = get_validator_for("components/populate")
    validator.validate(populate.as_dict())


def test_populate_value():
    """ Test populate class with optional value parameters """
    populate = Populate(validators=[greater_than_zero()], value=12)
    validator = get_validator_for("components/populate")
    validator.validate(populate.as_dict())


def test_populate_value_path():
    """ Test populate exceptions raised by passing both value and path arguments """
    with pytest.raises(InvalidArguments):
        Populate(
            validators=[greater_than_zero()],
            path="$.pick_details.quants[?(@.product.barcode == 'product')].qty",
            value=12,
        )


def test_populate_without_value_path():
    """ Test populate exceptions raised by not passing optional value and path arguments """
    with pytest.raises(InvalidArguments):
        Populate(validators=[greater_than_zero()])
