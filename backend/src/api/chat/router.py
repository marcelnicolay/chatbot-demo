from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from src.config import Settings, get_settings
from src.config import Settings, get_settings
from .schemas import ChatMessage, ChatRequest, MessageRole
from .models import ChatMessageInDB
from .service import ChatService
from src.api.threads.service import ThreadService


router = APIRouter()


@router.post("/")
async def chat(
    chat_request: ChatRequest,
    id: str, 
    settings: Annotated[Settings, Depends(get_settings)],
    thread_service: ThreadService = Depends(ThreadService),
    chat_service: ChatService = Depends(ChatService)
)->ChatMessage:
    thread = await thread_service.get(id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    if len(chat_request.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    
    lastMessage = chat_request.messages.pop()

    if lastMessage.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )
    
    return await chat_service.handle_message(settings, thread, lastMessage, messages=chat_request.messages)
    