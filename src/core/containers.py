from .translate import Translatable


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
