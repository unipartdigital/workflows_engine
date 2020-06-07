from functools import partial

from ..core.validators import Validator
from ..utils import func_factory, make_identifier
from . import defaults

__all__ = (
    "is_int",
    "greater_than_zero",
    "is_true",
    "is_false",
    "is_equal",
)

_make_identifier = partial(make_identifier, suffixes=[])

_is_int = func_factory(defaults.is_int, Validator, _make_identifier)
_greater_than_zero = func_factory(defaults.greater_than_zero, Validator, _make_identifier)
_is_equal = func_factory(defaults.is_equal, Validator, _make_identifier)


def is_int(value_key=None, **kwargs):
    kwargs["value_key"] = value_key
    return _is_int(**kwargs)


def greater_than_zero(value_key=None, **kwargs):
    kwargs["value_key"] = value_key
    return _greater_than_zero(**kwargs)


def is_equal(value_key=None, validator_key=None, validator_value=None, **kwargs):
    kwargs.update(
        {
            "value_key": value_key,
            "validator_key": validator_key,
            "validator_value": validator_value,
        }
    )
    return _is_equal(**kwargs)


def is_true(value_key=None, **kwargs):
    return is_equal(value_key=value_key, validator_value=True, identifier="is_true", **kwargs)


def is_false(value_key=None, **kwargs):
    return is_equal(value_key=value_key, validator_value=False, identifier="is_false", **kwargs)
