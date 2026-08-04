import os
from typing import Dict, Any

from .theme_agent import ThemeAgent
from .clustering_agent import ClusteringAgent
from .prioritization_agent import PrioritizationAgent
from .prd_agent import PRDAgent
from .roadmap_agent import RoadmapAgent

class OrchestratorAgent:
    """
    The Orchestrator controls the flow of data between all specialized PM agents.
    It executes the full product discovery pipeline end-to-end.
    """
    def __init__(self):
        print("Initializing Orchestrator Agent...")
        self.theme_agent = ThemeAgent()
        self.clustering_agent = ClusteringAgent()
        self.prioritization_agent = PrioritizationAgent()
        self.prd_agent = PRDAgent()
        self.roadmap_agent = RoadmapAgent()

    def run_full_pipeline(self) -> Dict[str, str]:
        """
        Executes the entire product pipeline and returns all intermediate and final outputs
        so they can be displayed on the Streamlit frontend.
        """
        print("\n--- STAGE 1: Extracting Themes ---")
        themes = self.theme_agent.extract_themes()
        
        print("\n--- STAGE 2: Clustering Initiatives ---")
        clusters = self.clustering_agent.cluster_themes(themes_text=themes)
        
        print("\n--- STAGE 3: Prioritizing (RICE Scoring) ---")
        priorities = self.prioritization_agent.prioritize_features(clusters_text=clusters)
        
        print("\n--- STAGE 4: Drafting Top Priority PRD ---")
        prd = self.prd_agent.generate_prd(prioritized_features_text=priorities)
        
        print("\n--- STAGE 5: Drafting Execution Roadmap ---")
        roadmap = self.roadmap_agent.generate_roadmap(prioritized_features_text=priorities)
        
        print("\n Full Pipeline Execution Complete!")
        
        # Return everything in a dictionary so the frontend can build nice tabs for each step
        return {
            "themes": themes,
            "clusters": clusters,
            "priorities": priorities,
            "prd": prd,
            "roadmap": roadmap
        }