import os
import chromadb
from typing import List, Dict, Any
from .base_agent import BaseAgent

class ThemeAgent(BaseAgent):
    """
    The Theme Agent is responsible for analyzing raw customer feedback 
    and extracting recurring themes, pain points, and feature requests.
    """
    def __init__(self):
        # Initialize the BaseAgent with a specific PM role and goal
        super().__init__(
            role="Product Manager - User Insights Specialist",
            goal="Analyze raw customer feedback, identify recurring themes, and summarize pain points objectively."
        )
        
        # Connect to ChromaDB to read the feedback
        db_path = os.getenv("CHROMADB_PATH", "./data/chroma_db")
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chroma_client.get_collection(name="product_feedback")

    def fetch_all_feedback(self) -> str:
        """Retrieves all feedback from the database and formats it into a single string."""
        try:
            data = self.collection.get()
            documents = data['documents']
            
            if not documents:
                return "No feedback found in the database."
                
            # Combine all feedback into a readable list for the LLM
            formatted_feedback = "\n".join([f"- {doc}" for doc in documents])
            return formatted_feedback
        except Exception as e:
            return f"Error fetching data: {str(e)}"

    def extract_themes(self) -> str:
        """
        Fetches data, builds a prompt, and asks the LLM to extract themes.
        """
        print("Theme Agent: Fetching feedback from Long-Term Memory...")
        context_data = self.fetch_all_feedback()
        
        if "No feedback found" in context_data or "Error" in context_data:
            return context_data

        print("Theme Agent: Analyzing data with AI...")
        
        # The specific instruction for the LLM
        prompt = (
            "Analyze the provided customer feedback. Group the feedback into 3 to 5 clear 'Product Themes'.\n"
            "For each theme, provide:\n"
            "1. Theme Name (e.g., 'Dashboard Performance')\n"
            "2. Brief Summary of the issue or request.\n"
            "3. Number of mentions (how many times it appears in the feedback).\n"
            "Format the output cleanly using Markdown."
        )
        
        # Call the LLM using the inherited run() method from BaseAgent
        response = self.run(prompt=prompt, context=context_data, temperature=0.3)
        return response