***********
Quick start
***********
.. testsetup::

    import json
    from workflows_engine import Workflow


.. testcode::

    import json
    from workflows_engine import Workflow, components, core

    not_zero_length = core.validators.Validator(
        identifier="not_zero_length",
        validator="isLength",
        validator_value=1,
        message_template="Field can not be empty",
    )

    class QuickWorkflow(Workflow):

        def flow(self):
            self.add_task(
                task_type="screen",
                name="InputMessage",
                components=[
                    core.components.Input(
                        label="Input message here",
                        destination_path="$.message",
                        validators=not_zero_length,
                    ),
                    components.buttons.submit()
                ],
            )

            self.add_task(
                task_type="screen",
                name="DisplayMessage",
                components=[
                    components.displays.info(
                        identifier="HelloWorldMessage",
                        template="{{$.message}}",
                    ),
                    components.buttons.next(text="Continue")
                ],
            )

            self.add_task(
                task_type="redirect",
                name="Restart",
                url="/api/quickstart"
            )

    print(json.dumps(QuickWorkflow().as_dict(), indent=4))

Produces the output:

.. testoutput::

    {
        "validators": {
            "not_zero_length": {
                "type": "isLength",
                "message": {
                    "type": "error",
                    "template": "Field can not be empty"
                },
                "valid_when": true,
                "validator_value": 1
            }
        },
        "components": {
            "input_": {
                "type": "input",
                "label": "Input message here",
                "target": "",
                "validator": [
                    "not_zero_length"
                ]
            },
            "submit_button": {
                "type": "button",
                "action": "submit",
                "style": "primary",
                "text": "Submit"
            },
            "HelloWorldMessage": {
                "type": "message_box",
                "message": {
                    "template": "{{$.message}}",
                    "type": "info"
                },
                "size": null
            },
            "next_button_next_primary_continue_buttons": {
                "type": "button",
                "action": "next",
                "style": "primary",
                "text": "Continue"
            }
        },
        "flow": {
            "type": "flow",
            "name": "QuickWorkflow",
            "tasks": [
                {
                    "type": "screen",
                    "name": "InputMessage",
                    "components": [
                        [
                            {
                                "name": "input_",
                                "destination_path": "$.message"
                            }
                        ],
                        [
                            {
                                "name": "submit_button"
                            }
                        ]
                    ],
                    "status_message": {
                        "type": "success",
                        "template": null
                    }
                },
                {
                    "type": "screen",
                    "name": "DisplayMessage",
                    "components": [
                        [
                            {
                                "name": "HelloWorldMessage"
                            }
                        ],
                        [
                            {
                                "name": "next_button_next_primary_continue_buttons"
                            }
                        ]
                    ],
                    "status_message": {
                        "type": "success",
                        "template": null
                    }
                },
                {
                    "type": "redirect",
                    "name": "Restart",
                    "url": "/api/quickstart"
                }
            ],
            "config": {}
        },
        "hash": "e1c8b005d184bbf5ce5fae9f7ac88e2930d151031bf3667734d25505d1d8966828a04fe796b7f9463799946a9901d26b75177d95044cb2a4cc9110645c0c308f",
        "context": {}
    }
