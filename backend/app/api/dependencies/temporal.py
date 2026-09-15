from typing import Annotated

from fastapi import Depends
from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter

from app.config import settings

_client: Client | None = None


async def get_temporal_client() -> Client:
    """Process-wide cached Temporal client, connected on first use."""
    global _client
    if _client is None:
        _client = await Client.connect(
            settings.temporal_address,
            namespace=settings.temporal_namespace,
            data_converter=pydantic_data_converter,
        )
    return _client


async def close_temporal_client() -> None:
    global _client
    _client = None


TemporalClient = Annotated[Client, Depends(get_temporal_client)]
