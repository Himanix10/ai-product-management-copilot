from typing import Optional
from pydantic import BaseModel

class FeedbackRecord(BaseModel):
    id: Optional[int] = None
    source: str
    user_type: str
    feedback_text: str
    category: str

class ClusterRecord(BaseModel):
    cluster_id: str
    area: str
    impact_area: str
    volume: int
    severity: str

class PriorityItem(BaseModel):
    id: Optional[int] = None
    title: str
    reach: float
    impact: float
    confidence: float
    effort: float
    rice_score: Optional[float] = None
    status: Optional[str] = "Planned"

class PRDDocument(BaseModel):
    id: Optional[int] = None
    feature_name: str
    target_persona: str
    problem_statement: str
    requirements: str
    markdown_content: Optional[str] = ""