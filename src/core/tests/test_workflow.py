import pytest
from workflows_engine import Workflow
from workflows_engine import validators
from workflows_engine.core import containers
from .schema_validator import get_validator_for


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
                    containers.PayloadPath(source_path="$.arg1", destination_path="$.arg1_result"),
                    containers.PayloadPath(source_path="$.arg2", destination_path="$.arg2_result"),
                ],
                payload={"arg1_result": None, "arg2_result": None},
                response_path="$.response",
            )

    return WorkflowTest


def test_flow_to_dict(workflow):
    workflow_dict = workflow(context={"value": "a"}).as_dict()
    validator = get_validator_for("workflow")
    validator.validate(workflow_dict)
