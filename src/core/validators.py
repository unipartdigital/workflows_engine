from .translate import Translatable

__all__ = ("Validator",)


class Validator:
    """Used to define a validator to be used in workflows

    args:
        identifer: str
            The name of validator workflows object is should be unique for a given set of input
            parameters. This value is used to lookup the validator config from the ``validator``

        validator: str
            The type of validator function to be used

        value_key: str (default=None)
            A jsonpath which points to the ``value`` to be compared with. This is ignored when the
            validator is attached to a field as the ``value`` used is the field's value. If None
            then "value_key" is not added to the dict represention

        validator_value: Any (default=None)
            The ``comparison value``. If None then "validator_value" is not added to the
            dict represention

        validator_key: str (default=None)
            A jsonpath which points to the ``comparison value``. If None then "validator_key" is
            not added to the dict represention

        valid_when: bool (default=True)
            Is used defined which return value means the check is valid. If False this essinatally
            can act as a negation of the return value of the ``validator`` function.
    """

    __slots__ = [
        "identifier",
        "validator",
        "value_key",
        "validator_value",
        "validator_key",
        "valid_when",
        "message",
        "__weakref__",
    ]

    def __init__(
        self,
        identifier,
        validator,
        value_key=None,
        validator_value=None,
        validator_key=None,
        message=None,
        valid_when=True,
    ):
        self.identifier = identifier
        self.validator = validator
        self.value_key = value_key
        self.validator_value = validator_value
        self.validator_key = validator_key
        self.message = message
        self.valid_when = valid_when

    def __iter__(self):
        yield self

    def get_message(self):
        if self.message:
            return self.message.as_dict()
        return None

    def as_dict(self):
        """Get dict represention of the validator"""
        validator = {
            "type": self.validator,
            "message": self.get_message(),
            "valid_when": self.valid_when,
        }
        if self.value_key is not None:
            validator["value_key"] = self.value_key

        if self.validator_value is not None:
            validator["validator_value"] = self.validator_value

        elif self.validator_key is not None:
            validator["validator_key"] = self.validator_key

        return validator
