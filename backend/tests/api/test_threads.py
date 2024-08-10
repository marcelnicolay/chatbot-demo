import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_thread_create(client: TestClient) -> None:
    response = client.post("/api/threads/")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "created_at" in data
