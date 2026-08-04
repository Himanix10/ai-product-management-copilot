import os
import sys

# Add the root project directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.agents.theme_agent import ThemeAgent

def test_theme_extraction():
    print("---  Starting Theme Agent Test ---")
    
    # Initialize and run the agent
    agent = ThemeAgent()
    
    print("\nExecuting extraction...\n")
    print("-" * 50)
    
    # Run the agent
    result = agent.extract_themes()
    
    # Print the AI's response
    print(result)
    print("-" * 50)
    print("\n Theme extraction complete!")

if __name__ == "__main__":
    test_theme_extraction()