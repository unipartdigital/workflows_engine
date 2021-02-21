Extending workflows
###################

Workflows is meant to be extensible, this is typically achieved by defining a new class from scratch or from an existing class via inheritance, through use of a subclass. The need for workflows extension arises from requiring a new type of action you wish to perform, one which is not currently supported, such as evaluating a novel piece of JS.

.. note:: This methodology of having the extension code written separately as an "addon" is likely the way we take on contributions from outside the core team.

.. warning:: If you choose to define something which is not supported by default you are breaking client compatibility. In this instance do not expect other implementations to be fully compatible with your workflows.

.. important:: Of course the examples given here are for illustrative purposes and will only define the json, it is up to the client to interpret it.



Adding new tasks types
**********************

Adding tasks to the workflows_engine is simple, the complicating aspect will always be the parsing and execution of the task.
The primary concern, of which to be wary, is that you must extend ``TASK_TYPE_MAPPING`` within ``workflows_engine.core.tasks`` otherwise ``Flow.add_task`` will not pick up the new task. This is the approach to use in order to overwrite behavior of a predefined task, but should be used with caution.


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

    # Update the task type mapping such that add_task can process the task
    TASK_TYPE_MAPPING["evil_eval"] = EvilEval


Usage
-----

.. code-block:: python

    from workflows_engine import Workflow

    class EvilThings(Workflow):

        def flow(self):
            self.add_task(
                task_type="evil_eval",
                name="IEvil",
                js_code="alert('evil is afoot');"
            )

Adding new components
*********************

The approach for adding new components is practically identical to that of adding a new task, we simply define a new class.


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
                A jsonpath pointing to a list of dicts, where
                the keys of each dict is one of the headers

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
                components=[
                    Table(
                        headers="$.table.headers",
                        rows="$.table.rows"
                    )
                ],
            )


    context = {
        "table": {
            "headers":["c1", "c2"],
            "rows": [
                {"c1": "c1r1", "c2": "c2r1"},
                {"c1": "c1r2", "c2": "c2r2"},
                {"c1": "c1r3", "c2": "c2r3"},
            ]
        }
    }
    workflow = ShouldIShowATable(context=context).as_dict()
    print(json.dumps(workflow, indent=4))



Adding new validators
*********************

Defining new validator types (not a vanilla functional type, requiring only a different string in the validator ``type`` keywords, but one requiring new keywords) would be similar to adding a new component, the main difference being that there is not currently a base class for ``Validators``.


Definition
----------

.. code-block:: python

    from workflows_engine.core.translate import Translatable

    class JSONRPCValidator:
        """
        A validator which calls an endpoint (see jsonrpc
        task for more details)
        """

        __slots__ = [
            "identifier",
            "validator",
            "url",
            "payload_paths",
            "payload",
            "message",
        ]



        def __init__(
            self,
            identifier,
            url,
            payload_paths,
            payload,
            message=None,
            valid_when=True,
        ):
            self.identifier = identifier
            self.validator = "jsonrpc"
            self.url = url
            self.payload_paths = payload_paths
            self.payload = payload
            self.message = message
            self.valid_when = valid_when

        def __iter__(self):
            yield self

        def get_message(self):
            if self.message:
                return self.message.as_dict()
            return None

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


Usage
-----

.. code-block:: python

    from myaddon.validator import JSONRPCValidator
    from workflows_engine import Workflow, components

    class ShouldIShowATable(Workflow):

        def flow(self):
            self.add_task(
                task_type="screen",
                name="HelloWorld",
                preconditions=JSONRPCValidator(
                    url="/api/should/I/show/myself",
                    payload_paths=[
                        {
                            "value": "HelloTable",
                            "result_key": "$.workflow.name"
                        }
                    ],
                    payload={"workflow": {"name": None}}
                ),
                components=[
                    Table(
                        headers="$.table.headers",
                        rows="$.table.rows"
                    )
                ],
            )

    context = {
        "table": {
            "headers":["c1", "c2"],
            "rows": [
                {"c1": "r1c1", "c2": "r1c2"},
                {"c1": "r2c1", "c2": "r2c2"},
                {"c1": "r3c1", "c2": "r3c2"},
            ]
        }
    }
    workflow = ShouldIShowATable(context=context).as_dict()
    print(json.dumps(, indent=4))
