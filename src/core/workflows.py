import json
from hashlib import sha512

from .tasks import Flow

__all__ = ("Workflow",)


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

    def _get_flow_no_context(self):
        if self.flow_cache is None:
            self.flow_cache = {
                "validators": self.base_flow_task.get_validators(),
                "components": self.base_flow_task.get_base_components(),
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
        """ Returns base flow task.

        Method to override to make the flow.
        """
        return NotImplementedError()
