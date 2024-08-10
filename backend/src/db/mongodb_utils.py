from motor.motor_asyncio import AsyncIOMotorClient
from src.config import Settings, get_settings
from .mongodb import db
from beanie import init_beanie
from src.api.threads.models import ThreadInDb


async def connect_to_mongo():
    settings: Settings = get_settings()
    db_client = AsyncIOMotorClient(settings.mongo_uri)
    await init_beanie(db_client.chatbot, document_models=[ThreadInDb])
    db.client = db_client


async def close_mongo_connection():
    db.client.close()
