# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Project configuration
    PROJECT_NAME: str = "FastAPI Chat"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "A real-time chat application built with FastAPI and WebSockets - for FE coding test use"
    
    # Service configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Log configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DIR: str = "logs"
    
    class Config:
        env_file = ".env"