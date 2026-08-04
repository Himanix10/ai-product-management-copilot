import os
import sys

# Add the root project directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.agents.orchestrator_agent import OrchestratorAgent

def test_orchestrator():
    print(" Starting Master Orchestrator Test\n" + "="*40)
    
    # 1. Initialize the Master Controller
    orchestrator = OrchestratorAgent()
    
    # 2. Run the entire pipeline with one command
    results = orchestrator.run_full_pipeline()
    
    # 3. Verify the final package
    print("\n" + "="*40)
    print(" FINAL DATA PACKAGE PREPARED FOR FRONTEND")
    print("="*40)
    print("Contains Keys:", list(results.keys()))
    
    print("\n Previewing the beginning of the generated PRD:\n")
    # Print just the first 300 characters of the PRD to prove it worked
    print(results["prd"][:300] + "...\n\n[End of preview]")

if __name__ == "__main__":
    test_orchestrator()