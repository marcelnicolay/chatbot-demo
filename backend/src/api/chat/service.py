from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from src.api.threads.models import ThreadInDb
from src.config import Settings

from .models import ChatMessageInDB
from .schemas import ChatMessage, MessageRole


class ChatService:
    
    async def save_message(self, thread: ThreadInDb, chat_message: ChatMessage) -> ChatMessage:
        """Create a new chat message."""
        chat_message_in_db = ChatMessageInDB(
            role=chat_message.role,
            content=chat_message.content,
            thread_id=thread.id
        )
        await chat_message_in_db.create()
        return ChatMessage(**chat_message_in_db.model_dump())

    def get_llm_model(self, settings: Settings) -> ChatOpenAI:
        llm_model = ChatOpenAI(
            model=settings.model,
            streaming=True,
            callbacks=[],
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            verbose=True,
        )
        
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content="You are a helpful assistant. Answer all questions to the best of your ability."),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | llm_model
        return chain
    
    def get_chat_history_from_messages(self, messages: List[ChatMessage]) -> ChatPromptTemplate:
        chat_history = []
        for message in messages:
            if message.role == MessageRole.USER:
                chat_history.append(
                    HumanMessage(content=message.content)
                )
            elif message.role == MessageRole.ASSISTANT:
                chat_history.append(
                    AIMessage(content=message.content)
                )
        return chat_history
    
    async def handle_message(self, settings: Settings, thread: ThreadInDb, last_message: ChatMessage, messages: List[ChatMessage]) -> List[ChatMessage]:
        await self.save_message(thread, last_message)

        llm_model = self.get_llm_model(settings)        

        chat_history = self.get_chat_history_from_messages(messages=messages)
        chat_history.append(
            HumanMessage(content=last_message.content)
        )

        response = await llm_model.ainvoke({"messages": chat_history})

        chat_message = ChatMessage(role=MessageRole.ASSISTANT, content=response.content)
        return await self.save_message(thread, chat_message)


