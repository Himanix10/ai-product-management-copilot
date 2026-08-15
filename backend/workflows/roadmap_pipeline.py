from agents.roadmap_agent import RoadmapAgent

def run_roadmap_pipeline():
    agent = RoadmapAgent()
    return agent.execute({})["schedule"]