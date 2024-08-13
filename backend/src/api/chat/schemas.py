from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class MessageRole(str, Enum):
    """Message role."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    id: str = None
    role: MessageRole
    content:str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
