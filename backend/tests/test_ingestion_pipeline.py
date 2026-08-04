import os
import sys

# Add the root project directory to the python path so we can import the backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.agents.ingestion_agent import IngestionAgent

def test_ingestion():
    print("---  Starting Ingestion Pipeline Test ---")
    
    print("\n1. Initializing Ingestion Agent...")
    agent = IngestionAgent()
    
    # Locate the mock data we just created
    mock_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/sample_feedback.csv'))
    
    if not os.path.exists(mock_file):
        print(f" Error: Could not find mock file at {mock_file}")
        return

    print(f"\n2. Processing mock data file: {os.path.basename(mock_file)}")
    result = agent.process_and_store([mock_file])
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    
    print("\n3. Verifying data inside ChromaDB (Long-Term Memory)...")
    docs = agent.collection.get()
    
    total_records = len(docs['ids'])
    print(f"Total records found in DB: {total_records}")
    
    if total_records > 0:
        print("\n Success! Data is safely stored. Here is the first record it found:")
        print(f"   Content: '{docs['documents'][0]}'")
        print(f"   Metadata: {docs['metadatas'][0]}")
    else:
        print("\n Warning: No records found in the database. Something went wrong.")

if __name__ == "__main__":
    test_ingestion()