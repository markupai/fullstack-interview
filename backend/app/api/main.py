from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies.temporal import close_temporal_client
from app.api.routers import set_up_routers


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    # The Temporal client connects lazily on first use (see dependencies/temporal.py)
    # so the API can boot and serve /health before Temporal is reachable.
    try:
        yield
    finally:
        await close_temporal_client()


app = FastAPI(title="Interview API", lifespan=lifespan)
set_up_routers(app)
