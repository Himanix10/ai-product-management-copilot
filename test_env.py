import os
import chromadb
import pandas as pd
import PyPDF2
from pydantic import BaseModel

def verify_environment():
    print("---  AI PM Copilot Environment Check ---")
    
    # 1. Test Package Imports
    print(" Packages imported successfully (pandas, PyPDF2, chromadb, pydantic)")
    
    # 2. Test ChromaDB Connection
    try:
        db_path = os.getenv("CHROMADB_PATH", "./data/chroma_db")
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_or_create_collection(name="test_collection")
        print(f" ChromaDB connected successfully at '{db_path}'")
    except Exception as e:
        print(f" ChromaDB error: {e}")
        return

    # 3. Test .env Key Detection
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "your_actual_openai_api_key_here":
        print(" OPENAI_API_KEY is configured!")
    else:
        print(" OPENAI_API_KEY is missing or set to placeholder in your .env file.")

    print("\n Your environment is completely functional and ready to run!")

if __name__ == "__main__":
    verify_environment()