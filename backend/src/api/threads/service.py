from src.config import Settings, get_settings

from .schemas import Thread
from .models import ThreadInDb
from src.errors import NoResultFound
from datetime import datetime
import uuid

class ThreadService:

    async def create(self) -> Thread:
        # TODO implement authentication
        
        thread = ThreadInDb(
            user_id=uuid.uuid4()
        )
        await thread.create()
        
        return Thread(**thread.model_dump())
        
    async def get(self, id: str) -> Thread:
        try:
            thread = await ThreadInDb.get(id)
        except ValueError:
            raise NoResultFound("Thread not found")
        
        if not thread:
            raise NoResultFound("Thread not found")
        
        return Thread(**thread.model_dump())
