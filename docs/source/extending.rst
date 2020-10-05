Extending workflows
###################

Workflows is meant to be extensible this is mainly done defining new class either by subclassing. Things which may require you to extend workflows are things like a new type of action you wish to preform like some form which is not currently supported like evaluating a piece of JS.

.. note:: This methodology of having the extension code written separately as an "addon" is likely the way we take on contributions from outside the core team.

.. warning:: If choose to defined something which is not supported by the default case you are breaking client compatibility.

.. important:: Of course the examples here will only define the json it is up to the client to interpret it.



Adding new tasks types
**********************

Adding tasks to the workflows_engine is simple the complicated bit will always be the parsing and execution of the task.
The only thing to wary of is that you must extend ``TASK_TYPE_MAPPING`` within ``workflows_engine.core.tasks`` otherwise ``Flow.add_task`` will not pick up you new task. This is also how you could overwrite behavior of a predefined task.


Definition
----------

.. code-block:: python

    from workflows_engine.core.tasks import Task, TASK_TYPE_MAPPING

    class EvilEval(Task):
        """Task to do evil things"""

        def __init__(
            self,
            name,
            js_code,
            preconditions=None,
        ):
            super().__init__(
                name=name,
                preconditions=preconditions,
                task_type="evil_eval",
            )
            self.js_code = js_code

        def as_dict(self):
            evil = super().as_dict()
            evil["code"] = self.js_code
            return evil

    # Update the task type mapping so add_task can process the task
    TASK_TYPE_MAPPING["evil_eval"] = EvilEval


Usage
-----

.. code-block:: python

    from workflows_engine import Workflow

    class QuickWorkflow(Workflow):

        def flow(self):
            self.add_task(
                task_type="evil_eval",
                name="IEvil",
                js_code="alert('evil things are happening');"
            )

Adding new components
*********************

Adding new components is very similar to adding a new task in that we simply define a new class.


Definition
----------

.. code-block:: python

    from workflows_engine.core.components import Component

    class Table(Component):
        """A component which displays a table

        Args:
            headers: str
                A jsonpath pointing to a list of strings
            rows: str
                A jsonpath point to a list of dicts, where the keys of each dict is one of the headers

        """

        __slots__ = [
            "headers",
            "rows",
        ]

        def __init__(self, headers, rows, **kwargs):
            super().__init__(**kwargs)
            self.headers = headers
            self.rows = rows

        def get_base_component_dict(self):
            return {
                "type": "table",
                "headers": self.headers,
                "rows": self.rows,
            }

Usage
-----

.. code-block:: python

    from myaddon.components import Table
    from workflows_engine import Workflow, components

    class QuickWorkflow(Workflow):

        def flow(self):
            self.add_task(
                task_type="screen",
                name="HelloWorld",
                components=[Table(headers="$.headers")],
            )

    print(json.dumps(QuickWorkflow().as_dict(), indent=4))



Adding new validators
*********************

Defining new validators types (not the normal functional type which just require different string in the validator ``type`` keywords - requiring new keywords) would be similar to adding a new component except there is not currently as base class for ``Validators``.


Definition
----------

.. code-block:: python

    from workflows_engine.core.translate import Translatable

    class Validator:
        """A validator which calls an endpoint see jsonrpc task for more details"""

        __slots__ = [
            "identifier",
            "validator",
            "url",
            "payload_paths",
            "payload",
            "__weakref__", # Required for translate to work.
        ]

        message_template = Translatable()

        def __init__(
            self,
            identifier,
            url,
            payload_paths,
            payload,
            message_template=None,
            valid_when=True,
        ):
            self.identifier = identifier
            self.validator = "jsonrpc"
            self.url = url
            self.payload_paths = payload_paths
            self.payload = payload
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
                "url": self.url,
                "payload_paths": self.payload_paths,
                "payload": self.payload,
                "valid_when": self.valid_when,
            }

            return validator



