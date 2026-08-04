import os
import sys

# Add the root project directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.agents.prioritization_agent import PrioritizationAgent
from backend.agents.roadmap_agent import RoadmapAgent

def test_roadmap_generation():
    print("---  Starting Roadmap Agent Test ---")
    
    # 1. We use the Mock Prioritization output to feed into the Roadmap Agent
    prioritization_agent = PrioritizationAgent()
    mock_priorities = prioritization_agent._generate_mock_response()
    
    print("\n[Step 1] Initializing Roadmap Agent...")
    roadmap_agent = RoadmapAgent()
    
    # 2. Generate the Roadmap
    print("\n[Step 2] Generating Roadmap based on Priorities...\n")
    roadmap_result = roadmap_agent.generate_roadmap(prioritized_features_text=mock_priorities)
    
    # 3. Print the final document
    print("="*60)
    print("  FINAL PRODUCT ROADMAP")
    print("="*60)
    print(roadmap_result)
    print("="*60)
    print("\n Roadmap Generation complete!")

if __name__ == "__main__":
    test_roadmap_generation()