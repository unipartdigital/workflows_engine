import pytest

from workflows_engine.core.tasks import Flow


@pytest.fixture
def flow():
    return Flow()


def test_add_task_to_flow(flow):
    task = flow.add_task(
        task_type="jsonrpc",
        name="task",
        url="/enpoint/task/url",
        method="GET",
        payload_paths=[
            {"key": "$.arg1", "result_key": "$.arg1_result"},
            {"key": "$.arg2", "result_key": "$.arg2_result"},
        ],
        payload={"arg1_result": None, "arg2_result": None},
        response_path="$.response",
    )

    assert task in flow.tasks, "Tasks do not contain result of add_task"
