from collections.abc import AsyncIterator

import httpx
import pytest

from app.api.main import app


@pytest.fixture
async def api() -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def test_health(api: httpx.AsyncClient) -> None:
    response = await api.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
