import os
import sys

# Add the root project directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.agents.theme_agent import ThemeAgent
from backend.agents.clustering_agent import ClusteringAgent
from backend.agents.prioritization_agent import PrioritizationAgent

def test_full_pipeline():
    print("---  Starting Full Agent Pipeline Test ---")
    
    # 1. Theme Agent
    print("\n[Step 1/3] Running Theme Agent...")
    theme_agent = ThemeAgent()
    themes = theme_agent.extract_themes()
    
    # 2. Clustering Agent
    print("\n[Step 2/3] Running Clustering Agent...")
    clustering_agent = ClusteringAgent()
    clusters = clustering_agent.cluster_themes(themes_text=themes)
    
    # 3. Prioritization Agent
    print("\n[Step 3/3] Running Prioritization Agent...")
    prioritization_agent = PrioritizationAgent()
    ranked_features = prioritization_agent.prioritize_features(clusters_text=clusters)
    
    # Print the final output
    print("\n" + "="*60)
    print(" FINAL DELIVERABLE: RANKED PRODUCT ROADMAP")
    print("="*60)
    print(ranked_features)
    print("="*60)
    print("\n Full pipeline test complete!")

if __name__ == "__main__":
    test_full_pipeline()