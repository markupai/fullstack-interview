from pydantic import BaseModel


class HelloRequest(BaseModel):
    name: str


class HelloStarted(BaseModel):
    workflow_id: str


class HelloResult(BaseModel):
    workflow_id: str
    status: str
    greeting: str | None = None
