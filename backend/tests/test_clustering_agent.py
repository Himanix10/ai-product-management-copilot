import os
import sys

# Add the root project directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.agents.theme_agent import ThemeAgent
from backend.agents.clustering_agent import ClusteringAgent

def test_pipeline():
    print("---  Starting Agent Pipeline Test (Theme -> Clustering) ---")
    
    # 1. Run the Theme Agent first
    print("\n[Step 1] Running Theme Agent...")
    theme_agent = ThemeAgent()
    themes_result = theme_agent.extract_themes()
    
    print(" Themes Extracted!")
    
    # 2. Pass the results to the Clustering Agent
    print("\n[Step 2] Running Clustering Agent...")
    clustering_agent = ClusteringAgent()
    clusters_result = clustering_agent.cluster_themes(themes_text=themes_result)
    
    # 3. Print the final output
    print("\n" + "="*50)
    print(" FINAL OUTPUT FROM CLUSTERING AGENT:")
    print("="*50)
    print(clusters_result)
    print("="*50)
    print("\n Pipeline test complete!")

if __name__ == "__main__":
    test_pipeline()