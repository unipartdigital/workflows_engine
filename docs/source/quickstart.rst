***********
Quick start
***********
.. testsetup::

    import json
    from workflows_engine import Workflow

Below can be found a simple example of a workflow implementation and the resultant workflow json. It is simply a screen with an input and a submit button. The input field itself is subject to a validator, this checks that the length of an input given is greater than 0. When the button is clicked either the validator error message will be shown below the input (should the length be 0 i.e. an empty input) or the user will progress to another screen, which will present an info box containing the string input into the field.
This acts to demonstrate several concepts described elsewhere, such as the validation of an input and transition between screen components, as well as more technical curiosities such as implementing a new validator. This is not intended to serve as an exhaustive representation of workflows, but simply a gentle introduction into how it can be put together.

.. testcode::

    import json
    from workflows_engine import Workflow, components, core, validators, containers

    not_zero_length = core.validators.Validator(
        identifier="not_zero_length",
        validator="isLength",
        validator_value=1,
        message=containers.message.error(template="Field can not be empty")
    )

    should_save_message = validators.is_true(
        identifier="should_save_message",
        value_key="$.save"
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
                    components.buttons.next(
                        text="Reset",
                        destination_path="$.save",
                        value=False
                    ),
                    components.buttons.next(
                        text="Save Message",
                        destination_path="$.save",
                        value=True
                    ),
                ],
            )

            self.add_task(
                task_type="jsonrpc",
                name="SaveMessage",
                preconditions=should_save_message,
                url="/api/save",
                payload_paths=[{"key": "$.message", "result_key": "$.message"}],
                payload={"message_to_save": None, "token": "RequestToken!"}
            )

            self.add_task(
                task_type="redirect",
                name="Restart",
                url="/api/quickstart" # This is the url which serves the workflow
            )

    print(json.dumps(QuickWorkflow().as_dict(), indent=4))

The workflow produced will be:

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
            },
            "should_save_message": {
                "type": "equals",
                "message": {
                    "type": "error",
                    "template": "Error: equals to values"
                },
                "valid_when": true,
                "value_key": "$.save",
                "validator_value": true
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
            "next_button_next_primary_reset_save_false_buttons": {
                "type": "button",
                "action": "next",
                "style": "primary",
                "text": "Reset",
                "value": false,
                "destination_path": "$.save"
            },
            "next_button_next_primary_save_message_save_true_buttons": {
                "type": "button",
                "action": "next",
                "style": "primary",
                "text": "Save Message",
                "value": true,
                "destination_path": "$.save"
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
                                "name": "next_button_next_primary_reset_save_false_buttons",
                                "destination_path": "$.save"
                            }
                        ],
                        [
                            {
                                "name": "next_button_next_primary_save_message_save_true_buttons",
                                "destination_path": "$.save"
                            }
                        ]
                    ],
                    "status_message": {
                        "type": "success",
                        "template": null
                    }
                },
                {
                    "type": "jsonrpc",
                    "name": "SaveMessage",
                    "preconditions": [
                        "should_save_message"
                    ],
                    "url": "/api/save",
                    "method": null,
                    "payload_paths": [
                        {
                            "key": "$.message",
                            "result_key": "$.message"
                        }
                    ],
                    "payload": {
                        "message_to_save": null,
                        "token": "RequestToken!"
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
        "hash": "9cf31161ba636e33af9d2160a7d7e0fb0efa6a62dadde9b479b054c84f2513df763b98830c09dc43caceccbf5154e203e6ac3bb169902fcbc919001d64b6b4d3",
        "context": {}
    }
