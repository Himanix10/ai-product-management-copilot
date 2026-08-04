import os
import sys

# Add the root project directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.agents.prioritization_agent import PrioritizationAgent
from backend.agents.prd_agent import PRDAgent

def test_prd_generation():
    print("---  Starting PRD Agent Test ---")
    
    # 1. We use the Mock Prioritization output to feed into the PRD Agent
    prioritization_agent = PrioritizationAgent()
    mock_priorities = prioritization_agent._generate_mock_response()
    
    print("\n[Step 1] Initializing PRD Agent...")
    prd_agent = PRDAgent()
    
    # 2. Generate the PRD
    print("\n[Step 2] Generating PRD based on #1 Priority Feature...\n")
    prd_result = prd_agent.generate_prd(prioritized_features_text=mock_priorities)
    
    # 3. Print the final document
    print("="*60)
    print("  FINAL ENGINEERING DELIVERABLE")
    print("="*60)
    print(prd_result)
    print("="*60)
    print("\n PRD Generation complete!")

if __name__ == "__main__":
    test_prd_generation()