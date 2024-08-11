from pydantic import Field, field_validator
from datetime import datetime
from beanie import Document
from .schemas import MessageRole


class ChatMessageInDB(Document):
    thread_id: str
    role: MessageRole
    created_at: datetime = Field(default_factory=datetime.now)
    message: str
