__all__ = (
    "is_int",
    "greater_than_zero",
    "is_equal",
)


is_int = dict(
    identifier="is_int", validator="isInt", message_template="Error: Field is not a whole number",
)

greater_than_zero = dict(
    identifier="greater_than_zero",
    validator="greaterThan",
    validator_value=0,
    message_template="Error: Value less than zero",
)

is_equal = dict(
    identifier="is_equal", validator="equals", message_template="Error: equals to values",
)
