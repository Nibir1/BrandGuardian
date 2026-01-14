"""
ingestion.py
------------
ETL Script to load raw text files into the Vector Database.
Usage: python -m src.services.ingestion
"""

import os
import glob
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.retrieval import get_vector_store
from src.config import settings

def load_documents(directory: str) -> List:
    """
    Loads all .txt files from the specified directory.
    """
    documents = []
    # Find all .txt files
    file_paths = glob.glob(os.path.join(directory, "*.txt"))
    
    if not file_paths:
        print(f"⚠️  No text files found in {directory}")
        return []

    print(f"📂 Found {len(file_paths)} documents to ingest.")
    
    for file_path in file_paths:
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
            print(f"   - Loaded: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"   ❌ Error loading {file_path}: {e}")
            
    return documents

def split_text(documents: List):
    """
    Splits documents into smaller chunks for better retrieval accuracy.
    Chunk size 500 is good for capturing full "paragraphs" of style.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50, # Overlap ensures context isn't lost at cut points
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✂️  Split {len(documents)} docs into {len(chunks)} chunks.")
    return chunks

def ingest_data():
    """
    Main execution function.
    """
    # 1. Define source directory
    source_dir = "data/brand_voice"
    
    # 2. Load
    raw_docs = load_documents(source_dir)
    if not raw_docs:
        return

    # 3. Split
    chunks = split_text(raw_docs)

    # 4. Store (Embed & Upsert)
    print("🧠 Initializing Vector Store...")
    vector_store = get_vector_store()
    
    print("🚀 Embedding and storing vectors... (This may take a moment)")
    vector_store.add_documents(chunks)
    
    # Chroma automatically persists, but explicit call is good practice in older versions
    # vector_store.persist() 
    
    print("✅ Ingestion Complete! Brand memory updated.")

if __name__ == "__main__":
    ingestion_start_msg = """
    ===========================================
      BrandGuardian | Knowledge Ingestion
    ===========================================
    """
    print(ingestion_start_msg)
    ingestion_done = ingest_data()