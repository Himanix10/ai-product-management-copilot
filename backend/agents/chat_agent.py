import os
import chromadb
from .base_agent import BaseAgent

class ChatAgent(BaseAgent):
    """
    The Chat Agent acts as an interactive Q&A assistant for the Product Manager.
    It uses RAG (Retrieval-Augmented Generation) to search the vector database 
    for relevant feedback and answers ad-hoc questions.
    """
    def __init__(self):
        super().__init__(
            role="Product Manager - Conversational Insights Assistant",
            goal="Answer user queries accurately and conversationally using specific context retrieved from the product feedback database."
        )
        
        db_path = os.getenv("CHROMADB_PATH", "./data/chroma_db")
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        
        # We use try/except in case the collection hasn't been created yet
        try:
            self.collection = self.chroma_client.get_collection(name="product_feedback")
        except Exception:
            self.collection = None

    def answer_query(self, user_query: str) -> str:
        """
        Takes a user's question, searches the database for relevant feedback, 
        and uses the LLM to generate an answer based on that context.
        """
        print(f"Chat Agent: Analyzing query -> '{user_query}'")
        
        if not self.collection:
            return "I cannot access the feedback database right now. Please ensure data has been ingested."

        print("Chat Agent: Retrieving relevant context from ChromaDB...")
        try:
            # We ask ChromaDB for the 5 pieces of feedback most mathematically similar to the question
            results = self.collection.query(
                query_texts=[user_query],
                n_results=5 
            )
            
            # Extract the raw text documents from the search results
            documents = results.get('documents', [[]])[0]
            
            if not documents:
                return "I couldn't find any relevant feedback in the database to answer your question."
                
            context_data = "Retrieved Feedback:\n" + "\n".join([f"- {doc}" for doc in documents])
            
        except Exception as e:
            return f"Error retrieving data from ChromaDB: {str(e)}"
            
        print("Chat Agent: Formulating answer...")
        prompt = (
            f"User Question: {user_query}\n\n"
            "Please answer the user's question directly based ONLY on the provided retrieved feedback context. "
            "Be conversational but concise. "
            "If the answer cannot be found in the provided context, politely state that you do not have enough data to answer."
        )
        
        # Call the LLM (Slightly higher temperature for a more conversational tone)
        return self.run(prompt=prompt, context=context_data, temperature=0.5)

    def _generate_mock_response(self) -> str:
        """Overrides the BaseAgent mock to return a chat-specific simulated response."""
        return (
            "### MOCK AI RESPONSE\n\n"
            "Based on the feedback in the database, users are primarily complaining about "
            "the dashboard loading slowly when they have more than 50 items. We also have multiple reports "
            "of the iOS app crashing. I highly recommend we prioritize a performance update!"
        )