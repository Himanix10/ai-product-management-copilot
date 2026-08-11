from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from backend.database.db import init_db, get_db
from backend.agents.orchestrator_agent import OrchestratorAgent
from backend.database.models import CustomerFeedback, OpportunityPrioritization

app = FastAPI(title="AI PM Copilot API", version="1.0")

@app.on_event("startup")
def startup():
    init_db()

orchestrator = OrchestratorAgent()

class FeedbackPayload(BaseModel):
    raw_feedback: List[Dict[str, Any]]

class ChatPayload(BaseModel):
    query: str

class RICEPayload(BaseModel):
    initiative_title: str
    reach: int
    impact: float
    confidence: float
    effort: float

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI PM Copilot Backend"}

@app.post("/api/v1/run-pipeline")
def run_pipeline(payload: FeedbackPayload, db: Session = Depends(get_db)):
    result = orchestrator.run(payload.model_dump())
    return result.data

@app.post("/api/v1/chat")
def chat(payload: ChatPayload):
    response = orchestrator.chat.run({"query": payload.query})
    return response.data

@app.post("/api/v1/prioritize")
def prioritize_initiative(payload: RICEPayload, db: Session = Depends(get_db)):
    score = (payload.reach * payload.impact * payload.confidence) / payload.effort if payload.effort > 0 else 0.0
    
    db_item = OpportunityPrioritization(
        initiative_title=payload.initiative_title,
        reach=payload.reach,
        impact=payload.impact,
        confidence=payload.confidence,
        effort=payload.effort,
        rice_score=score
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return {"priority_id": db_item.priority_id, "rice_score": round(score, 2)}

@app.get("/api/v1/feedback")
def get_feedback(db: Session = Depends(get_db)):
    return db.query(CustomerFeedback).all()