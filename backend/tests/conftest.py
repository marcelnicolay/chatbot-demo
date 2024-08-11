"""Pytest fixtures."""
from collections.abc import AsyncIterator
import pytest_asyncio
from src.main import app
from asgi_lifespan import LifespanManager
from httpx import AsyncClient


@pytest_asyncio.fixture()
async def client() -> AsyncIterator[AsyncClient]:
    """Async server client that handles lifespan and teardown."""
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as _client:
                yield _client