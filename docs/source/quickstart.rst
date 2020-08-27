***********
Quick start
***********
.. testsetup::

    import json
    from workflows_engine import Workflow


.. testcode::

    import json
    from workflows_engine import Workflow

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
                "msg_template": "HelloWorld",
                "msg_type": "info"
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
                    "status_msg": {
                        "type": "success",
                        "template": null
                    }
                }
            ]
        },
        "hash": "e3e43453336b67ff57d8e06508c45871f7066b33ebf18c91a954212348fa5bbb4cd8f68e5375c657b565c99ac276439d6e522b040610b659547c6029e73437e4",
        "context": {}
    }
