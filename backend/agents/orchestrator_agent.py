from backend.agents.base_agent import BaseAgent
from backend.agents.ingestion_agent import IngestionAgent
from backend.agents.theme_agent import ThemeAgent
from backend.agents.clustering_agent import ClusteringAgent
from backend.agents.prioritization_agent import PrioritizationAgent
from backend.agents.prd_agent import PRDAgent
from backend.agents.roadmap_agent import RoadmapAgent
from backend.agents.chat_agent import ChatAgent
from typing import Dict, Any

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="OrchestratorAgent",
            system_prompt="Coordinates sub-agent workflows and manages pipeline execution."
        )
        self.ingestion = IngestionAgent()
        self.theme = ThemeAgent()
        self.clustering = ClusteringAgent()
        self.prioritization = PrioritizationAgent()
        self.prd = PRDAgent()
        self.roadmap = RoadmapAgent()
        self.chat = ChatAgent()

    def _process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        state = {}
        state.update(self.ingestion.run(input_data).data)
        state.update(self.theme.run(state).data)
        state.update(self.clustering.run(state).data)
        state.update(self.prioritization.run(state).data)
        state.update(self.prd.run(state).data)
        state.update(self.roadmap.run(state).data)
        return {"status": "Pipeline Execution Successful", "results": state}