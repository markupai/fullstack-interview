import logging

from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.worker import Worker

from app.activities.hello import compose_greeting
from app.config import settings
from app.workflows.hello import HelloWorkflow

WORKFLOWS = [HelloWorkflow]
ACTIVITIES = [compose_greeting]


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect(
        settings.temporal_address,
        namespace=settings.temporal_namespace,
        data_converter=pydantic_data_converter,
    )
    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=WORKFLOWS,
        activities=ACTIVITIES,
    )
    logging.info("worker listening on task queue %r", settings.temporal_task_queue)
    await worker.run()
