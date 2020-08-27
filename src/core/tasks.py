from itertools import chain
from threading import RLock
from functools import partial

__all__ = (
    "Task",
    "Screen",
    "JsonRpc",
    "Update",
    "Redirect",
    "LocalStore",
    "DomainParam",
    "ClearDomainParams",
    "Condition",
    "Flow",
    "WhileLoop",
)


class Task:
    __slots__ = [
        "name",
        "task_type",
        "preconditions",
    ]

    def __init__(self, name=None, preconditions=None, task_type=""):
        self.name = name
        self.preconditions = preconditions
        self.task_type = task_type

    def as_dict(self):
        base = {
            "type": self.task_type,
            "name": self.name,
        }

        preconditions = self.get_preconditions()
        if preconditions:
            base["preconditions"] = preconditions

        return base

    def get_base_components(self):
        return {}

    def get_result(self):
        return {}

    def get_validators(self):
        if self.preconditions:
            return {key: value for p in self.preconditions for key, value in p.as_dict().items()}
        else:
            return {}

    def get_preconditions(self):
        if self.preconditions:
            return [p.identifier for p in self.preconditions]
        else:
            return None


class Screen(Task):
    __slots__ = [
        "components",
        "status_msg_template",
        "show_status_msg",
    ]

    def __init__(
        self,
        name,
        preconditions=None,
        components=None,
        status_msg_template=None,
        show_status_msg=True,
    ):
        super().__init__(name=name, preconditions=preconditions, task_type="screen")
        self.components = components
        self.status_msg_template = status_msg_template
        self.show_status_msg = show_status_msg

    def get_flow_components(self):
        return [[c.get_flow_component_dict() for c in row] for row in self.components]

    def get_base_components(self):
        return {
            key: value
            for row in self.components
            for c in row
            for key, value in c.get_base_component_dict().items()
        }

    def get_validators(self):
        validators = super().get_validators()
        validators.update(
            {
                key: value
                for row in self.components
                for c in row
                for key, value in c.get_validators().items()
            }
        )
        return validators

    def get_status_msg(self):
        msg = {
            "type": "success",
            "template": self.status_msg_template,
        }
        return msg

    def as_dict(self):
        screen = super().as_dict()
        screen["components"] = self.get_flow_components()

        if self.show_status_msg:
            screen["status_msg"] = self.get_status_msg()

        return screen


class JsonRpc(Task):
    __slots__ = [
        "url",
        "method",
        "payload_paths",
        "payload",
        "response_path",
    ]

    def __init__(
        self,
        name,
        preconditions=None,
        url=None,
        method=None,
        payload_paths=None,
        payload=None,
        response_path=None,
    ):
        super().__init__(name=name, preconditions=preconditions, task_type="jsonrpc")
        self.url = url
        self.method = method
        self.payload_paths = payload_paths or []
        self.payload = payload or {}
        self.response_path = response_path

    def get_payload(self):
        return self.payload

    def get_payload_paths(self):
        return self.payload_paths

    def as_dict(self):
        endpoint = super().as_dict()
        endpoint.update(
            {
                "url": self.url,
                "method": self.method,
                "payload_paths": self.get_payload_paths(),
                "payload": self.get_payload(),
            }
        )
        if self.response_path:
            endpoint["response_path"] = self.response_path
        return endpoint


class Update(Task):
    __slots__ = [
        "tasks",
    ]

    def __init__(self, name, preconditions=None, tasks=None):
        super().__init__(name=name, preconditions=preconditions, task_type="update")
        self.tasks = tasks

    def get_tasks(self):
        return self.tasks

    def as_dict(self):
        update = super().as_dict()
        update["tasks"] = self.get_tasks()
        return update


class Redirect(Task):
    __slots__ = [
        "url",  # url to redirect to
    ]

    def __init__(self, name, preconditions=None, url=""):
        super().__init__(name=name, preconditions=preconditions, task_type="redirect")
        self.url = url

    def as_dict(self):
        update = super().as_dict()
        update["url"] = self.url
        return update


class LocalStore(Task):
    __slots__ = [
        "context_path",  # JSON path to context variable to copy to local storage
        "storage_key",  # key in local storage to store value
    ]

    def __init__(self, name, preconditions=None, context_path="", storage_key=""):
        super().__init__(name=name, preconditions=preconditions, task_type="set_local_storage")
        self.context_path = context_path
        self.storage_key = storage_key

    def as_dict(self):
        update = super().as_dict()
        update.update(
            {"context_path": self.context_path, "storage_key": self.storage_key,}
        )
        return update


class DomainParam(Task):
    # Todo: explain the purpose of this
    __slots__ = [
        "context_path",  # JSON path to context variable to copy to local storage
        "param",  # name of parameter
    ]

    def __init__(self, name, preconditions=None, context_path="", param=""):
        super().__init__(name=name, preconditions=preconditions, task_type="set_domain_param")
        self.context_path = context_path
        self.param = param

    def as_dict(self):
        domain = super().as_dict()
        domain.update(
            {"context_path": self.context_path, "param": self.param,}
        )
        return domain


class ClearDomainParams(Task):
    __slots__ = []

    def __init__(self, name, **kwargs):
        super().__init__(name=name, task_type="clear_domain_params", **kwargs)


class Condition(Task):
    __slots__ = [
        "conditions",
        "tasks",
        "on_success",  # Flow step name on success
        "success_message",
        "on_failure",  # Flow step name on failure
        "failure_message",
    ]

    def __init__(
        self,
        name=None,
        conditions=None,
        preconditions=None,
        on_success=None,
        success_message=None,
        on_failure=None,
        failure_message=None,
    ):
        super().__init__(name=name, preconditions=preconditions, task_type="condition")
        self.conditions = conditions
        self.on_success = on_success
        self.success_message = success_message
        self.on_failure = on_failure
        self.failure_message = failure_message

    @staticmethod
    def get_message(message):
        msg = {"type": message.message_type, "template": message.template}
        return msg

    def get_conditions(self):
        return [c.identifier for c in self.conditions]

    def get_validators(self):
        validators = super().get_validators()
        validators.update(
            {key: value for c in self.conditions for key, value in c.as_dict().items()}
        )
        return validators

    def as_dict(self):
        condition = super().as_dict()
        condition.update(
            {
                "conditions": self.get_conditions(),
                "on_success": self.on_success,
                "on_failure": self.on_failure,
                "success_message": self.get_message(self.success_message),
                "failure_message": self.get_message(self.failure_message),
            }
        )
        return condition


class Flow(Task):
    __slots__ = [
        "tasks",
        "result",
        "result_keys",
        "destination_path",
        "conditions",
        "iterable_path",
        "sub_type",
        "config",
        "_lock",
    ]

    def __init__(
        self,
        name=None,
        preconditions=None,
        tasks=None,
        result_keys=None,
        result=None,
        destination_path=None,
        sub_type="flow",
        conditions=None,
    ):
        super().__init__(name=name, preconditions=preconditions, task_type="flow")
        self.tasks = tasks or []
        self.result = result
        self.destination_path = destination_path
        self.result_keys = result_keys
        self.conditions = conditions or []
        self.sub_type = sub_type
        self._lock = RLock()

    def get_validators(self):
        validators = super().get_validators()
        validators.update(
            {key: value for c in self.conditions for key, value in c.as_dict().items()}
        )
        return validators

    def get_config(self):
        builders = {
            "flow": lambda inst: (
                {
                    "result": inst.result,
                    "result_keys": inst.result_keys,
                    "destination_path": inst.destination_path,
                }
                if inst.result and inst.result_keys and inst.destination_path is not None
                else {}
            ),
            "while_loop": lambda inst: {
                "conditions": [c.identifier for c in inst.conditions],
                "result": inst.result,
                "result_keys": inst.result_keys,
                "destination_path": inst.destination_path,
            },
            "for_loop": lambda inst: {
                "iterable_path": inst.iterable_path,
                "destination_path": inst.destination_path,
                "result": inst.result,
                "result_keys": inst.result_keys,
            },
        }

        return builders[self.sub_type](self)

    @staticmethod
    def add_task_type(name, task_class):
        TASK_TYPE_MAPPING[name] = task_class

    def get_tasks(self):
        return [t.as_dict() for t in self.tasks]

    def get_base_components(self):
        return {key: value for t in self.tasks for key, value in t.get_base_components().items()}

    def get_validators(self):
        validators = super().get_validators()
        validators.update(
            {key: value for t in self.tasks for key, value in t.get_validators().items()}
        )
        return validators

    def as_dict(self):
        flow = super().as_dict()
        flow["tasks"] = self.get_tasks()

        # Note: destination_path could be false as this means that the result object should be merged
        # directly into the context
        if self.result_keys and self.result and self.destination_path is not None:
            flow.update(config=self.get_config())
        return flow

    def add_task(self, task_type, name, **kwargs):
        task = TASK_TYPE_MAPPING[task_type](name=name, **kwargs)
        with self._lock:
            self.tasks.append(task)
        return task

    def clear_tasks(self):
        with self._lock:
            self.tasks = []


class Event(Task):
    __slots__ = [
        "action",
        "payload",
    ]

    def __init__(self, action, payload=None, **kwargs):
        super().__init__(task_type="event", **kwargs)
        self.action = action
        self.payload = payload or {}


TASK_TYPE_MAPPING = {
    "screen": Screen,
    "jsonrpc": JsonRpc,
    "local_store": LocalStore,
    "update": Update,
    "redirect": Redirect,
    "condition": Condition,
    "domain_param": DomainParam,
    "flow": Flow,
    "while_loop": partial(Flow.__init__, sub_type="while_loop"),
    "for_loop": partial(Flow.__init__, sub_type="for_loop"),
    "clear_domain_params": ClearDomainParams,
}