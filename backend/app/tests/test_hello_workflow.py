import uuid

from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from app.activities.hello import compose_greeting
from app.workflows.hello import HelloInput, HelloWorkflow


async def test_hello_workflow_greets() -> None:
    async with await WorkflowEnvironment.start_time_skipping(
        data_converter=pydantic_data_converter
    ) as env:
        task_queue = f"test-{uuid.uuid4()}"
        async with Worker(
            env.client,
            task_queue=task_queue,
            workflows=[HelloWorkflow],
            activities=[compose_greeting],
        ):
            result = await env.client.execute_workflow(
                HelloWorkflow.run,
                HelloInput(name="Ada"),
                id=f"hello-{uuid.uuid4()}",
                task_queue=task_queue,
            )
    assert result.greeting == "Hello, Ada!"
