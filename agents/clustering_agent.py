from typing import Dict, Any
from agents.base_agent import BaseAgent
from backend.tools.db_tools import DBTools

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False


class ClusteringAgent(BaseAgent):
    def __init__(self):
        super().__init__("ClusteringAgent")

    def execute(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        feedback_df = DBTools.get_feedback_records()

        if not SKLEARN_AVAILABLE or feedback_df.empty or len(feedback_df) < 3:
            pain_points_df = DBTools.get_pain_points()
            records = pain_points_df.to_dict(orient="records") if not pain_points_df.empty else [
                {
                    "Cluster ID": "PP-DEFAULT-1",
                    "Pain Point Area": "Integration & Sync Latency",
                    "Impact Area": "Webhook sync delays",
                    "Support Volume": 120,
                    "Severity": "High Friction"
                }
            ]
            return {
                "agent": self.agent_name,
                "clusters": records,
                "total_clustered": len(records)
            }

        try:
            texts = feedback_df["Feedback"].tolist()
            vectorizer = TfidfVectorizer(stop_words="english", min_df=1)
            tfidf_matrix = vectorizer.fit_transform(texts)

            best_k = 2
            best_score = -1
            max_possible_k = min(len(texts) - 1, 6)

            if max_possible_k >= 2:
                for k in range(2, max_possible_k + 1):
                    km = KMeans(n_clusters=k, random_state=42, n_init=5)
                    labels = km.fit_predict(tfidf_matrix)
                    score = silhouette_score(tfidf_matrix, labels)
                    if score > best_score:
                        best_score = score
                        best_k = k

            final_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
            feedback_df["Cluster_Group"] = final_kmeans.fit_predict(tfidf_matrix)

            clusters = []
            for group_id, group in feedback_df.groupby("Cluster_Group"):
                sample_text = group["Feedback"].iloc[0]
                clusters.append({
                    "Cluster ID": f"PP-DYNAMIC-{group_id + 100}",
                    "Pain Point Area": f"Cluster {group_id + 1} ({len(group)} items)",
                    "Impact Area": str(sample_text)[:35] + "...",
                    "Support Volume": len(group) * 50,
                    "Severity": "High Friction" if len(group) >= 3 else "Medium Friction"
                })

            return {
                "agent": self.agent_name,
                "clusters": clusters,
                "optimal_k": best_k,
                "total_clustered": len(texts)
            }
        except Exception:
            pain_points_df = DBTools.get_pain_points()
            return {
                "agent": self.agent_name,
                "clusters": pain_points_df.to_dict(orient="records"),
                "total_clustered": len(pain_points_df)
            }