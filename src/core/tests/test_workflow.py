import pytest
from workflows_engine import Workflow
from workflows_engine import validators


@pytest.fixture
def workflow():
    class WorkflowTest(Workflow):
        def flow(self):
            self.add_task(
                task_type="jsonrpc",
                name="task",
                url="/endpoint/task/url",
                preconditions=validators.is_equal(value_key="$.value", validator_value="a"),
                method="GET",
                payload_paths=[
                    {"key": "$.arg1", "result_key": "$.arg1_result"},
                    {"key": "$.arg2", "result_key": "$.arg2_result"},
                ],
                payload={"arg1_result": None, "arg2_result": None},
                response_path="$.response",
            )

    return WorkflowTest


def test_flow_to_dict(workflow):
    assert workflow(context={"value": "a"}).as_dict() == {
        "validators": {
            "equals_value_a": {
                "equals_value_a": {
                    "type": "equals",
                    "message": {"type": "error", "template": "Error: equals to values"},
                    "valid_when": True,
                    "value_key": "$.value",
                    "validator_value": "a",
                }
            }
        },
        "components": {},
        "flow": {
            "type": "flow",
            "name": "WorkflowTest",
            "tasks": [
                {
                    "type": "jsonrpc",
                    "name": "task",
                    "preconditions": ["equals_value_a"],
                    "url": "/endpoint/task/url",
                    "method": "GET",
                    "payload_paths": [
                        {"key": "$.arg1", "result_key": "$.arg1_result"},
                        {"key": "$.arg2", "result_key": "$.arg2_result"},
                    ],
                    "payload": {"arg1_result": None, "arg2_result": None},
                    "response_path": "$.response",
                }
            ],
        },
        "hash": "8dc828bab468306772d69c761b5395768903add89133d783a25265c555e2916230c0efddafb48e19c2509b049c07b586d929fa624c8bcbb0319ee2abb1762dfa",
        "context": {"value": "a"},
    }
