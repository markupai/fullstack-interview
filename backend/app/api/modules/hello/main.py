import uuid

from fastapi import APIRouter
from temporalio.client import WorkflowExecutionStatus

from app.api.dependencies.temporal import TemporalClient
from app.api.modules.hello.schemas import HelloRequest, HelloResult, HelloStarted
from app.config import settings
from app.workflows.hello import HelloInput, HelloWorkflow

hello_router = APIRouter(prefix="/hello", tags=["hello"])


@hello_router.post("", status_code=202)
async def start_hello(body: HelloRequest, client: TemporalClient) -> HelloStarted:
    handle = await client.start_workflow(
        HelloWorkflow.run,
        HelloInput(name=body.name),
        id=f"hello-{uuid.uuid4()}",
        task_queue=settings.temporal_task_queue,
    )
    return HelloStarted(workflow_id=handle.id)


@hello_router.get("/{workflow_id}")
async def get_hello(workflow_id: str, client: TemporalClient) -> HelloResult:
    handle = client.get_workflow_handle_for(HelloWorkflow.run, workflow_id)
    description = await handle.describe()
    status = description.status or WorkflowExecutionStatus.RUNNING
    greeting = None
    if status == WorkflowExecutionStatus.COMPLETED:
        greeting = (await handle.result()).greeting
    return HelloResult(workflow_id=workflow_id, status=status.name, greeting=greeting)
