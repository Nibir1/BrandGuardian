"""
retrieval.py
------------
Manages the Vector Database connection and Embedding logic.
This module is responsible for initializing ChromaDB with the correct
embedding model (OpenAI).
"""

import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.config import settings

def get_embedding_function():
    """
    Returns the OpenAI Embedding function using the API key from settings.
    We use 'text-embedding-3-small' for cost-efficiency and high performance.
    """
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.OPENAI_API_KEY
    )

def get_vector_store():
    """
    Initializes and returns the ChromaDB vector store.
    It points to the local persistence directory defined in config.
    """
    embedding_fn = get_embedding_function()
    
    # Ensure directory exists
    os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
    
    vector_store = Chroma(
        persist_directory=settings.CHROMA_DB_PATH,
        embedding_function=embedding_fn,
        collection_name=settings.CHROMA_COLLECTION_NAME
    )
    
    return vector_store