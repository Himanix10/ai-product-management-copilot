from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="AI PM Copilot API Service", version="1.0.0")

class RICEPayload(BaseModel):
    title: str
    reach: float
    impact: float
    confidence: float
    effort: float

class ChatQuery(BaseModel):
    prompt: str

FEEDBACK_DATA = [
    {"ID": 101, "Source": "Zendesk", "User": "Enterprise Lead", "Feedback": "Need faster PRD exports and bulk actions", "Category": "Feature Request"},
    {"ID": 102, "Source": "Survey", "User": "Product Mgr", "Feedback": "UI navigation is crisp and modern", "Category": "Usability"},
    {"ID": 103, "Source": "CRM", "User": "Tech Lead", "Feedback": "Add REST API webhooks for Jira synchronization", "Category": "Integration"},
    {"ID": 104, "Source": "Email", "User": "SaaS Founder", "Feedback": "Dashboard queries experience latency delays", "Category": "Bug"},
]

@app.get("/")
def root():
    return {"status": "ok", "service": "AI PM Copilot Backend API"}

@app.get("/api/feedback")
def get_feedback(category: Optional[str] = "All"):
    if category and category != "All":
        return [item for item in FEEDBACK_DATA if item["Category"] == category]
    return FEEDBACK_DATA

@app.post("/api/priorities/rice")
def calculate_rice(payload: RICEPayload):
    if payload.effort <= 0:
        raise HTTPException(status_code=400, detail="Effort must be > 0.")
    score = (payload.reach * payload.impact * payload.confidence) / payload.effort
    return {"title": payload.title, "score": round(score, 2)}

@app.post("/api/chat")
def handle_chat(query: ChatQuery):
    return {"reply": f"AI Copilot: Processed request '{query.prompt}'"}
