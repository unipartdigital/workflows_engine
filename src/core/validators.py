from .translate import Translatable

__all__ = ("Validator",)


class Validator:
    __slots__ = [
        "identifier",
        "validator",
        "value_key",
        "validator_value",
        "validator_key",
        "valid_when",
        "__weakref__",
    ]

    message_template = Translatable()

    def __init__(
        self,
        identifier,
        validator,
        value_key=None,
        validator_value=None,
        validator_key=None,
        message_template=None,
        valid_when=True,
    ):
        self.identifier = identifier
        self.validator = validator
        self.value_key = value_key
        self.validator_value = validator_value
        self.validator_key = validator_key
        self.message_template = message_template or ""
        self.valid_when = valid_when

    def __iter__(self):
        yield self

    def get_message(self):
        return {"type": "error", "template": self.message_template}

    def as_dict(self):
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
