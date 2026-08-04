import os
import sys

# Add the root project directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.agents.chat_agent import ChatAgent

def test_chat_agent():
    print("---  Starting Chat Agent (RAG) Test ---")
    
    # Initialize the Chat Agent
    print("\n[Step 1] Initializing Chat Agent...")
    chat_agent = ChatAgent()
    
    # Define a test question
    test_question = "Are there any complaints about the mobile app or iOS?"
    
    # Ask the question
    print(f"\n[Step 2] Asking Question: '{test_question}'\n")
    response = chat_agent.answer_query(user_query=test_question)
    
    # Print the AI's answer
    print("="*60)
    print(" AI ASSISTANT ANSWER")
    print("="*60)
    print(response)
    print("="*60)
    print("\n Chat Agent test complete!")

if __name__ == "__main__":
    test_chat_agent()