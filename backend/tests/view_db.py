import os
import chromadb

def view_database():
    print("---  Opening Long-Term Memory (ChromaDB) ---")
    
    # 1. Connect to the database folder
    db_path = os.getenv("CHROMADB_PATH", "./data/chroma_db")
    client = chromadb.PersistentClient(path=db_path)
    
    try:
        # 2. Open our specific collection
        collection = client.get_collection(name="product_feedback")
    except Exception:
        print(" Error: Could not find the 'product_feedback' collection. Has ingestion run successfully?")
        return

    # 3. Fetch all records
    data = collection.get()
    total_records = len(data['ids'])
    
    print(f"\n Found {total_records} records in the database.\n")
    print("-" * 50)
    
    # 4. Print them out nicely
    for i in range(total_records):
        print(f" ID: {data['ids'][i]}")
        print(f" Content: {data['documents'][i]}")
        
        # Format metadata nicely
        metadata = data['metadatas'][i]
        print(f" Source: {metadata.get('source', 'Unknown')} | Sentiment: {metadata.get('sentiment', 'Unknown')}")
        print("-" * 50)

if __name__ == "__main__":
    view_database()