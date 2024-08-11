from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
from functools import lru_cache


import os
from pathlib import Path

parent_folder = Path(os.path.dirname(__file__)).parent


class Settings(BaseSettings):
    llm_temperature: float = 0.2 
    llm_max_tokens: int = 512
    top_k: int = 3
    openai_api_key: Optional[str]
    model: str = "gpt-3.5-turbo"
    embedding_model: str = "text-embedding-3-small"
    mongo_uri: str
    db_name: str = "chatbot"
    verbose: bool = True
    vectorstore_persist_directory: str = os.path.join(parent_folder, "data", "vectorstore")
    vectorstore_load_dir: str = os.path.join(parent_folder, "data", "load")

    model_config = SettingsConfigDict(env_file=".env", extra='ignore', env_nested_delimiter='__')


@lru_cache
def get_settings():
    return Settings()
