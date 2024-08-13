from fastapi.testclient import TestClient
from .data import create_thread, get_chat_by_id
import pytest

@pytest.mark.asyncio
async def test_chat_create(client: TestClient) -> None:
    thread = await create_thread()

    response = await client.post("/api/threads/{}/chat/".format(thread.id), json={"messages": [{"content": "Hello, World!", "role": "user"}]})
    assert response.status_code == 200
    data = response.json()

    chat_from_db = await get_chat_by_id(data['id'])
    
    assert data['role'] == "assistant"    
    assert data['content'] == chat_from_db.content
    assert str(thread.id) == chat_from_db.thread_id

@pytest.mark.asyncio
async def test_chat_create_no_messages(client: TestClient) -> None:
    thread = await create_thread()

    response = await client.post("/api/threads/{}/chat/".format(thread.id), json={"messages": []})
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_chat_create_last_message_not_user(client: TestClient) -> None:
    thread = await create_thread()

    response = await client.post("/api/threads/{}/chat/".format(thread.id), json={"messages": [{"content": "Hello, World!", "role": "assistant"}]})
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_chat_create_thread_not_found(client: TestClient) -> None:
    response = await client.post("/api/threads/1234/chat/", json={"messages": [{"content": "Hello, World!", "role": "user"}]})
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_chat_with_history(client: TestClient) -> None:
    thread = await create_thread()

    response = await client.post("/api/threads/{}/chat/".format(thread.id), json={
        "messages": [
            {"role": "user","content": "hello, my name is Johny"},
            {"role": "assistant",  "content": "Hello! How can I assist you today?"},
            {"role": "user", "content": "what is my name?"}
        ]
    })
    assert response.status_code == 200
    data = response.json()

    assert "Johny" in data['content']