from typing import Optional
from datetime import datetime
from pydantic import BaseModel
import uuid


class Thread(BaseModel):
    id: str
    created_at: datetime
    user_id: uuid.UUID

    class Config:
        from_attributes = True