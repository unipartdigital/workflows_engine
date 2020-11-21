from .translate import Translatable
from ..exceptions import InvalidArguments


class Container:
    __slots__ = ["__weakref__"]


class Message(Container):
    __slots__ = ["message_type"]

    template = Translatable()

    def __init__(self, template, message_type):
        self.template = template
        self.message_type = message_type

    def as_dict(self):
        return {"template": self.template, "type": self.message_type}


class TaskTarget(Container):
    __slots__ = ["flow", "task"]

    def __init__(self, flow_name, task_name):
        self.flow = flow_name
        self.task = task_name

    def as_dict(self):
        return {"flow": self.flow, "task": self.task}


class Populate(Container):
    __slots__ = ["path", "validators", "value"]

    def _validate_args(self, path, value):
        if value is not None and path is not None:
            raise InvalidArguments("'value' and 'path' attribute cannot be used together")
        if value is None and path is None:
            raise InvalidArguments("Either 'value' or 'path' attribute must be used")

    def __init__(self, validators, path=None, value=None, **kwargs):
        self._validate_args(path, value)
        super().__init__(**kwargs)
        self.path = path
        self.validators = validators
        self.value = value

    def get_validators(self):
        yield from self.validators

    def as_dict(self):
        res = {"validators": [v.identifier for v in self.validators]}
        if self.path:
            res["path"] = self.path
        if self.value:
            res["value"] = self.value
        return res


class PayloadPath(Container):
    __slots__ = ["value", "source_path", "destination_path"]

    def __init__(self, value=None, source_path=None, destination_path=None):
        if value is not None and source_path is not None:
            raise InvalidArguments("'value' and 'source_path' attribute cannot be used together")
        if value is None and source_path is None:
            raise InvalidArguments("Either 'value' or 'source_path' attribute must be used")

        self.value = value
        self.source_path = source_path
        self.destination_path = destination_path

    def as_dict(self):
        res = {"result_key": self.destination_path}
        if self.value:
            res["value"] = self.value
        else:
            res["key"] = self.source_path

        return res


class ContextUpdateInstruction(Container):
    __slots__ = [
        "value",
        "template",
        "source_path",
        "destination_path",
        "append",
        "extend",
    ]

    def __init__(
        self,
        value=None,
        template=None,
        source_path=None,
        destination_path=None,
        append=False,
        extend=False,
    ):
        src_keys = ["value", "template", "source_path"]
        src_vars_with_val = [x for x in src_keys if getattr(self, x) is not None]

        if len(src_vars_with_val) > 1:
            var_names = "' and '".join(src_vars_with_val)
            raise InvalidArguments(f"'{var_names}' attribute cannot be used together")
        elif len(src_vars_with_val) == 0:
            raise InvalidArguments(
                f"One of 'value', 'template' or 'source_path' attribute must be used"
            )

        if append is not False and extend is not False:
            raise InvalidArguments("'append' and 'extend' attribute cannot be used together")

        self.value = value
        self.template = template
        self.source_path = source_path
        self.destination_path = destination_path
        self.append = append
        self.extend = extend

    def as_dict(self):
        res = {"result_key": self.destination_path}
        if self.value:
            res["value"] = self.value
        elif self.template:
            res["template"] = self.template
        else:
            res["key"] = self.source_path

        if self.append:
            res["append"] = self.append
        elif self.extend:
            res["extend"] = self.extend

        return res
