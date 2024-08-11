from src.api.threads.models import ThreadInDb
from src.api.chat.models import ChatMessageInDB
import uuid


async def create_thread()->ThreadInDb:
    thread = ThreadInDb(
        user_id=uuid.uuid4()
    )
    await thread.create()
    return thread

async def get_chat_by_id(chat_id:str)->ChatMessageInDB:
    return await ChatMessageInDB.get(chat_id)
