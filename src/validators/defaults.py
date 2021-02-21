from ..containers import messages

__all__ = (
    "is_int",
    "greater_than_zero",
    "is_equal",
)


is_int = dict(
    identifier="is_int",
    validator="isInt",
    message=messages.error(template="Field is not a whole number"),
)

greater_than_zero = dict(
    identifier="greater_than_zero",
    validator="greaterThan",
    validator_value=0,
    message=messages.error(template="Value less than zero"),
)

is_equal = dict(
    identifier="is_equal",
    validator="equals",
    message=messages.error(template="Value equals to values"),
)
