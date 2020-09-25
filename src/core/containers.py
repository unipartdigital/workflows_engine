from .translate import Translatable
from ..exceptions import InvalidArguments


class Container:
    __slots__ = [
        "__weakref__",
    ]


class Message(Container):
    __slots__ = [
        "message_type",
    ]

    template = Translatable()

    def __init__(self, template, message_type):
        self.template = template
        self.message_type = message_type

    def as_dict(self):
        return {"template": self.template, "type": self.message_type}


class TaskTarget(Container):
    __slots__ = [
        "flow",
        "task",
    ]

    def __init__(self, flow_name, task_name):
        self.flow = flow_name
        self.task = task_name

    def as_dict(self):
        return {"flow": self.flow, "task": self.task}


class Populate(Container):
    __slots__ = ["path", "validators", "value"]

    def __init__(self, validators, path=None, value=None, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.validators = validators
        self.value = value
        if value and path:
            raise InvalidArguments("'value' and 'path' attribute cannot be used together")
        if not (value or path):
            raise InvalidArguments("Either 'value' or 'path' attribute must be used")

    def as_dict(self):
        retval = {"validators": [v.validator for v in self.validators]}
        if self.path:
            retval.update(path=self.path)
        if self.value:
            retval.update(value=self.value)
        return retval
