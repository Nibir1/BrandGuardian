"""
retrieval.py
------------
Manages the Vector Database connection and Embedding logic.
"""

import os
from typing import List
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.config import settings

def get_embedding_function():
    """
    Returns the OpenAI Embedding function using the API key from settings.
    """
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.OPENAI_API_KEY
    )

def get_vector_store() -> Chroma:
    """
    Initializes and returns the ChromaDB vector store.
    """
    embedding_fn = get_embedding_function()
    
    # Ensure directory exists to prevent errors on fresh clones
    os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
    
    vector_store = Chroma(
        persist_directory=settings.CHROMA_DB_PATH,
        embedding_function=embedding_fn,
        collection_name=settings.CHROMA_COLLECTION_NAME
    )
    
    return vector_store

def get_brand_retriever(k: int = 3):
    """
    Returns a retriever configured for 'Maximal Marginal Relevance' (MMR).
    
    Args:
        k (int): Number of documents to return.
        
    Returns:
        VectorStoreRetriever: Configured retriever object.
    """
    vector_store = get_vector_store()
    
    # MMR (Maximal Marginal Relevance) ensures we get diverse examples,
    # not just 3 versions of the exact same sentence.
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "fetch_k": 10,  # Fetch 10 candidates, select top k diverse ones
            "lambda_mult": 0.5  # Balance between relevance (1.0) and diversity (0.0)
        }
    )