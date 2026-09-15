from fastapi import APIRouter, FastAPI

from app.api.modules.hello.main import hello_router

health_router = APIRouter(tags=["health"])


@health_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


def set_up_routers(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(hello_router)
