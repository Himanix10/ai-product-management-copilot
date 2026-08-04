import os
import uuid
import re
import pandas as pd
import PyPDF2
import chromadb
from typing import List, Dict, Any
from pydantic import BaseModel

class FeedbackRecord(BaseModel):
    """
    Standardized data model for all incoming product feedback.
    This ensures the Theme and Clustering agents always receive consistent data.
    """
    id: str
    source: str
    content: str
    metadata: Dict[str, Any] = {}

class IngestionAgent:
    def __init__(self):
        """
        Initialize the agent and connect to the Long-Term Memory (ChromaDB).
        It uses the environment variable we set up earlier in the .env file.
        """
        # Fetch the DB path from environment variables, fallback to default
        db_path = os.getenv("CHROMADB_PATH", "./data/chroma_db")
        
        # Ensure the directory exists
        os.makedirs(db_path, exist_ok=True)
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        
        # Get or create a collection specifically for raw feedback
        self.collection = self.chroma_client.get_or_create_collection(
            name="product_feedback",
            metadata={"hnsw:space": "cosine"} # Cosine similarity for text search
        )

    def _clean_text(self, text: str) -> str:
        """
        Removes unnecessary whitespace, special characters, and normalizes text.
        """
        if not isinstance(text, str):
            return ""
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        # Remove non-ascii characters (optional, but helps clean noisy data)
        text = text.encode('ascii', 'ignore').decode('ascii')
        return text.strip()

    def _parse_txt(self, file_path: str) -> List[FeedbackRecord]:
        """Reads a standard text file and returns it as a single record."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        clean_content = self._clean_text(content)
        
        return [FeedbackRecord(
            id=str(uuid.uuid4()),
            source=os.path.basename(file_path),
            content=clean_content,
            metadata={"type": "txt"}
        )]

    def _parse_pdf(self, file_path: str) -> List[FeedbackRecord]:
        """Extracts text from a PDF page by page."""
        records = []
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    full_text += extracted + " "
                    
        clean_content = self._clean_text(full_text)
        
        records.append(FeedbackRecord(
            id=str(uuid.uuid4()),
            source=os.path.basename(file_path),
            content=clean_content,
            metadata={"type": "pdf"}
        ))
        return records

    def _parse_csv(self, file_path: str) -> List[FeedbackRecord]:
        """
        Parses a CSV file. Assumes there might be 'feedback', 'description', 
        or 'content' columns.
        """
        df = pd.read_csv(file_path)
        records = []
        
        # Try to guess the main text column if it exists
        text_cols = [col for col in df.columns if col.lower() in ['feedback', 'description', 'content', 'text']]
        main_col = text_cols[0] if text_cols else df.columns[0] # Fallback to first column
        
        for index, row in df.iterrows():
            raw_text = str(row[main_col])
            clean_content = self._clean_text(raw_text)
            
            if clean_content:
                # Store the rest of the row as metadata
                metadata = row.drop(main_col).to_dict()
                # Ensure all metadata values are strings, ints, or floats for ChromaDB compatibility
                metadata = {k: str(v) for k, v in metadata.items()} 
                metadata["type"] = "csv_row"
                metadata["row_index"] = str(index)
                
                records.append(FeedbackRecord(
                    id=str(uuid.uuid4()),
                    source=os.path.basename(file_path),
                    content=clean_content,
                    metadata=metadata
                ))
                
        return records

    def process_and_store(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Main entry point. Takes a list of file paths, parses them, 
        and stores the extracted documents into Long-Term Memory (ChromaDB).
        """
        all_records: List[FeedbackRecord] = []
        
        # 1. Parse all files based on their extension
        for path in file_paths:
            ext = path.lower().split('.')[-1]
            try:
                if ext == 'txt':
                    all_records.extend(self._parse_txt(path))
                elif ext == 'pdf':
                    all_records.extend(self._parse_pdf(path))
                elif ext == 'csv':
                    all_records.extend(self._parse_csv(path))
                else:
                    print(f"Unsupported file type: {ext}")
            except Exception as e:
                print(f"Error processing {path}: {str(e)}")
                
        if not all_records:
            return {"status": "error", "message": "No valid data extracted."}

        # 2. Prepare data for ChromaDB
        ids = [record.id for record in all_records]
        documents = [record.content for record in all_records]
        metadatas = [{"source": r.source, **r.metadata} for r in all_records]

        # 3. Store in Vector Database
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        
        return {
            "status": "success",
            "records_processed": len(all_records),
            "message": f"Successfully stored {len(all_records)} records in Long-Term Memory."
        }