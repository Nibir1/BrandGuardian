"""
config.py
---------
Centralized configuration management for BrandGuardian.
Uses Pydantic BaseSettings to validate environment variables on application startup.
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application Settings Model.
    Inherits from Pydantic BaseSettings for validation and type safety.
    """
    
    # API Configuration
    OPENAI_API_KEY: str # Required. App will fail if missing.
    
    # App General
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    API_V1_STR: str = "/api/v1"
    
    # Vector DB Configuration
    CHROMA_DB_PATH: str = "data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "vaisala_brand_voice"
    
    # RAG Settings
    RAG_SIMILARITY_THRESHOLD: float = 0.75

    # Configuration to read from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" # Ignore extra keys in .env
    )

@lru_cache()
def get_settings() -> Settings:
    """
    Creates and caches the Settings object.
    Using lru_cache ensures we don't read the .env file on every request.
    
    Returns:
        Settings: The validated configuration object.
    """
    return Settings()

# Global settings instance for easy import
settings = get_settings()