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
            user_id=uuid.uuid4(),
            created_at=datetime.now()
        )
        await thread.create()
        
        return Thread(**thread.model_dump())