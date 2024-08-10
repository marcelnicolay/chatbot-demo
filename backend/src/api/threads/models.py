from beanie import Document
from datetime import datetime
import uuid


class ThreadInDb(Document):
    created_at: datetime
    user_id: uuid.UUID
