from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import Settings, get_settings
from src.db.mongodb import get_database
from src.api.chat.router import router as ChatRouter
from .schemas import Thread
from .service import ThreadService


router = APIRouter()
router.include_router(ChatRouter, prefix="/{id}/chat")

@router.post("/", response_model=Thread)
async def create_thread(
    service: ThreadService = Depends(ThreadService)
):
    return await service.create()