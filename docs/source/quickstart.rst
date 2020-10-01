***********
Quick start
***********
.. testsetup::

    import json
    from workflows_engine import Workflow


.. testcode::

    import json
    from workflows_engine import Workflow, components

    class QuickWorkflow(Workflow):

        def flow(self):
            self.add_task(
                task_type="screen",
                name="HelloWorld",
                components=[
                    components.displays.info(
                        identifier="HelloWorldMessage",
                        template="HelloWorld",
                    )
                ],
            )

    print(json.dumps(QuickWorkflow().as_dict(), indent=4))

Produces the output:

.. testoutput::
    {
        "validators": {},
        "components": {
            "HelloWorldMessage": {
                "type": "message_box",
                "message": {
                    "template": "HelloWorld",
                    "type": "info"
                },
                "size": null
            }
        },
        "flow": {
            "type": "flow",
            "name": "QuickWorkflow",
            "tasks": [
                {
                    "type": "screen",
                    "name": "HelloWorld",
                    "components": [
                        [
                            {
                                "name": "HelloWorldMessage"
                            }
                        ]
                    ],
                    "status_message": {
                        "type": "success",
                        "template": null
                    }
                }
            ],
            "config": {}
        },
        "hash": "8320f02fe112dcf63e8f7b6f5d90f0959c100646eab295c2a45dd82b1d09fe20af976bcd20e74e22caf6b5750debaacb31e212777e505b31cdce540d1fd998d4",
        "context": {}
    }
