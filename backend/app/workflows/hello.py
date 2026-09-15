from datetime import timedelta

from pydantic import BaseModel
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from app.activities.hello import compose_greeting


class HelloInput(BaseModel):
    name: str


class HelloOutput(BaseModel):
    greeting: str


@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, input_data: HelloInput) -> HelloOutput:
        greeting = await workflow.execute_activity(
            compose_greeting,
            input_data.name,
            start_to_close_timeout=timedelta(seconds=10),
        )
        return HelloOutput(greeting=greeting)
