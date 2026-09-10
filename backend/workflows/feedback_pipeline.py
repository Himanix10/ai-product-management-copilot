from agents.ingestion_agent import IngestionAgent
from agents.theme_agent import ThemeAgent
from agents.clustering_agent import ClusteringAgent

def run_feedback_pipeline(source: str, user_type: str, text: str, category: str):
    ingest_agent = IngestionAgent()
    theme_agent = ThemeAgent()
    cluster_agent = ClusteringAgent()

    ingest_res = ingest_agent.execute({"source": source, "user_type": user_type, "text": text, "category": category})
    themes_res = theme_agent.execute({})
    cluster_res = cluster_agent.execute({"feedbacks": [ingest_res["cleaned_text"]]})

    return {
        "ingestion": ingest_res,
        "themes": themes_res["themes"],
        "clusters": cluster_res["clusters"]
    }