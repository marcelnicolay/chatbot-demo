import uuid
from datetime import datetime
from pydantic import Field
from beanie import Document


class ThreadInDb(Document):
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: uuid.UUID
