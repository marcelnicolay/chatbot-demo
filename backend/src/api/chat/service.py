from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from src.api.threads.models import ThreadInDb
from src.config import Settings
from src.retriever import vs

from .models import ChatMessageInDB
from .schemas import ChatMessage, MessageRole

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)


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
        """
        Conversational RAG implementation with chat history using langchain_openai
        using the built-in chain constructors from langchain.
        https://python.langchain.com/v0.2/docs/tutorials/qa_chat_history/
        """ 
        llm_model = ChatOpenAI(
            model=settings.model,
            streaming=True,
            callbacks=[],
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            verbose=True,
        )
        
        # takes historical messages and the latest user question, and reformulates the question
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=contextualize_q_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever  = create_history_aware_retriever(llm_model, vs.retriever, contextualize_q_prompt)

        # rephrasing of the input query to our retriever, so that the retrieval incorporates the context of the conversation
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        # use create_stuff_documents_chain to generate a question_answer_chain, with input keys context, chat_history, and input
        question_answer_chain = create_stuff_documents_chain(llm_model, qa_prompt)

        # This chain applies the history_aware_retriever and question_answer_chain in sequence
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        return rag_chain
    
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
        response = await llm_model.ainvoke({"chat_history": chat_history, "input": last_message.content})

        chat_message = ChatMessage(role=MessageRole.ASSISTANT, content=response['answer'])
        return await self.save_message(thread, chat_message)


