import json
from hashlib import sha512
from collections import defaultdict
from .tasks import Flow

__all__ = ("Workflow",)


class SameIdentiferDifferentValues(Exception):
    pass


def dict_to_set(d):
    return frozenset(
        (k, dict_to_set(v))
        if isinstance(v, dict)
        else (k, frozenset(v))
        if isinstance(v, list)
        else (k, v)
        for k, v in d.items()
    )


class Workflow:
    __slots__ = ["name", "base_flow_task", "hash", "flow_cache", "context"]

    def __init__(self, *args, context=None):
        self.context = context if context is not None else {}
        self.name = self.__class__.__name__
        self.base_flow_task = Flow(name=self.name)
        self.flow_cache = None
        self.hash = None
        self.build_flow(*args)

    @property
    def has_been_built(self):
        return self.flow_cache is not None

    @staticmethod
    def _get_parts(part_type, iters, dict_getter):
        result = {}
        part_cache = defaultdict(set)
        for part in iters:
            name = part.identifier
            part_dict = dict_getter(part)
            part_set = dict_to_set(part_dict)
            if name in result:
                if part_cache[name] != part_set:
                    message = "Two {part_type} with the same identifer({name}) but different values"
                    raise SameIdentiferDifferentValues(
                        message.format(part_type=part_type, name=name)
                    )
            else:
                result[name] = part_dict
                part_cache[name] = part_set

        return result

    def get_validators(self):
        """Get validator dicts"""
        return self._get_parts(
            "validators", self.base_flow_task.get_validators(), lambda x: x.as_dict()
        )

    def get_base_components(self):
        """Get component dicts"""
        return self._get_parts(
            "components",
            self.base_flow_task.get_base_components(),
            lambda x: x.get_base_component_dict(),
        )

    def _get_flow_no_context(self):
        if self.flow_cache is None:
            self.flow_cache = {
                "validators": self.get_validators(),
                "components": self.get_base_components(),
                "flow": self.base_flow_task.as_dict(),
            }
        return self.flow_cache

    def clear_cache(self):
        self.flow_cache = None
        self.hash = None

    def clear_flow(self):
        self.base_flow_task.clear_tasks()
        self.clear_cache()

    def get_hash(self):
        """Get hash of workflow json object not including the hash and context values"""

        if self.hash is None:
            if self.flow_cache is None:
                self._get_flow_no_context()
            self.hash = str(sha512(json.dumps(self.flow_cache).encode()).hexdigest())
        return self.hash

    def as_dict(self):
        """Build workflow dictionary to transform into JSON"""
        workflow = self._get_flow_no_context()
        workflow.update({"hash": self.get_hash(), "context": self.context})
        return workflow

    def add_task(self, *args, **kwargs):
        """Add task to main flow of the workflow"""
        return self.base_flow_task.add_task(*args, **kwargs)

    def build_flow(self, *args, **kwargs):
        self.clear_flow()
        self.flow(*args, **kwargs)

    def flow(self, *args, **kwargs):
        """Returns base flow task.

        Method to override to make the flow.
        """
        return NotImplementedError()
