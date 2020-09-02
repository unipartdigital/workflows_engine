__all__ = ("Validator",)


class Validator:
    __slots__ = [
        "identifier",
        "validator",
        "value_key",
        "validator_value",
        "validator_key",
        "msg_template",
        "valid_when",
    ]

    def __init__(
        self,
        identifier,
        validator,
        value_key=None,
        validator_value=None,
        validator_key=None,
        msg_template=None,
        valid_when=True,
    ):
        self.identifier = identifier
        self.validator = validator
        self.value_key = value_key
        self.validator_value = validator_value
        self.validator_key = validator_key
        self.msg_template = msg_template or ""
        self.valid_when = valid_when

    def __iter__(self):
        yield self

    def get_message(self):
        return {"type": "error", "template": self.msg_template}

    def as_dict(self):
        validator = {
            "type": self.validator,
            "msg": self.get_message(),
            "valid_when": self.valid_when,
        }
        if self.value_key is not None:
            validator["value_key"] = self.value_key

        if self.validator_value is not None:
            validator["validator_value"] = self.validator_value

        elif self.validator_key is not None:
            validator["validator_key"] = self.validator_key

        return {self.identifier: validator}
