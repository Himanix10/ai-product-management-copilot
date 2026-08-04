from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import os

from database.db import get_db
from database.models import (
    Feedback,
    Theme,
    Cluster,
    Priority,
    PRD,
    Roadmap,
    Workspace
)

router = APIRouter(tags=["AI Product Management API"])

# --- Request/Response Pydantic Models ---

class PrioritizeRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    reach: float
    impact: float
    confidence: float
    effort: float

class PRDRequest(BaseModel):
    feature_name: str
    problem_statement: str
    target_users: Optional[str] = "Existing product users"
    goals: Optional[str] = ""
    success_metrics: Optional[str] = ""
    user_stories: Optional[str] = ""
    acceptance_criteria: Optional[str] = ""
    dependencies: Optional[str] = ""
    risks: Optional[str] = ""

class RoadmapRequest(BaseModel):
    feature_name: str
    priority: str
    status: str
    owner: str
    quarter: str
    progress: int

class ChatRequest(BaseModel):
    prompt: str

# --- API Route Implementations ---

@router.get("/api/feedback")
def get_feedback_analysis(db: Session = Depends(get_db)):
    """Fetch synchronized feedback metrics, theme trends, and clusters from SQLite."""
    feedbacks = db.query(Feedback).all()
    themes_db = db.query(Theme).all()
    clusters_db = db.query(Cluster).all()

    # If empty, return a zero state or base structure
    if not feedbacks:
        return {
            "record_count": 0,
            "filename": "Connected Database Sync",
            "report": {"executive_summary": "No feedback records found in the database."},
            "themes": [],
            "clusters": [],
            "preview": []
        }

    # Theme Aggregation
    theme_counts = {}
    for t in themes_db:
        theme_counts[t.theme_name] = theme_counts.get(t.theme_name, 0) + 1
    themes_payload = [{"theme": k, "count": v} for k, v in theme_counts.items()]

    # Cluster Aggregation
    cluster_mentions = {}
    for t in themes_db:
        if t.cluster:
            cluster_name = t.cluster.cluster_name
            cluster_mentions[cluster_name] = cluster_mentions.get(cluster_name, 0) + 100 # weight metric
    clusters_payload = [{"cluster": k, "mentions": v} for k, v in cluster_mentions.items()]

    # Previews list
    preview_payload = []
    for f in feedbacks:
        preview_payload.append({
            "ID": f.id,
            "Source": f.source or "Database Sync",
            "User": f.customer or "Enterprise User",
            "Feedback": f.content,
            "Category": "Usability" if "speed" in f.content.lower() or "slow" in f.content.lower() else "Feature Request"
        })

    # Summary
    summary = f"Aggregated analysis of {len(feedbacks)} customer feedback records: "
    if theme_counts:
        top_theme = max(theme_counts, key=theme_counts.get)
        summary += f"Primary customer concern centers on '{top_theme}'. "
    summary += "Automated roadmap updates recommended based on priority scoring shifts."

    return {
        "record_count": len(feedbacks),
        "filename": "Connected SQLite Database",
        "report": {
            "executive_summary": summary
        },
        "themes": themes_payload,
        "clusters": clusters_payload,
        "preview": preview_payload
    }


@router.get("/api/features")
def get_prioritized_features(db: Session = Depends(get_db)):
    """Fetch prioritized features (RICE priority list) from SQLite."""
    priorities = db.query(Priority).join(Cluster).all()
    results = []
    for p in priorities:
        results.append({
            "name": p.cluster.cluster_name,
            "reach": p.reach,
            "impact": p.impact,
            "confidence": p.confidence,
            "effort": p.effort,
            "rice_score": p.rice_score,
            "priority": p.priority_level,
            "status": "Backlog"
        })
    return results


@router.post("/api/agents/prioritize")
def prioritize_feature(req: PrioritizeRequest, db: Session = Depends(get_db)):
    """Add a new feature and calculate its RICE priority score."""
    # Compute RICE
    rice = (req.reach * req.impact * req.confidence) / (req.effort if req.effort > 0 else 0.1)
    rice = round(rice, 1)

    # Determine priority tier
    if rice >= 1000:
        level = "High"
    elif rice >= 500:
        level = "Medium"
    else:
        level = "Low"

    # Save to SQLite
    # 1. Create a Cluster for the feature
    cluster = Cluster(
        cluster_name=req.name,
        summary=req.description
    )
    db.add(cluster)
    db.commit()
    db.refresh(cluster)

    # 2. Save RICE Priority details
    p = Priority(
        cluster_id=cluster.id,
        rice_score=rice,
        reach=int(req.reach),
        impact=req.impact,
        confidence=req.confidence,
        effort=req.effort,
        priority_level=level,
        scoring_method="RICE"
    )
    db.add(p)
    db.commit()

    return {
        "priority": level,
        "rice_score": rice,
        "recommendation": f"Feature '{req.name}' scoring completed. Calculated RICE index: {rice}. Prioritized as {level} priority."
    }


@router.post("/api/agents/generate-prd")
def generate_prd_document(req: PRDRequest, db: Session = Depends(get_db)):
    """Generate a structured Markdown PRD and save it to SQLite."""
    # Find or create a matching priority item
    cluster = db.query(Cluster).filter(Cluster.cluster_name == req.feature_name).first()
    if not cluster:
        cluster = Cluster(cluster_name=req.feature_name, summary=req.problem_statement)
        db.add(cluster)
        db.commit()
        db.refresh(cluster)

    priority = db.query(Priority).filter(Priority.cluster_id == cluster.id).first()
    if not priority:
        priority = Priority(
            cluster_id=cluster.id,
            rice_score=500.0,
            reach=1000,
            impact=2.0,
            confidence=0.8,
            effort=2.0,
            priority_level="Medium",
            scoring_method="RICE"
        )
        db.add(priority)
        db.commit()
        db.refresh(priority)

    # Render Markdown Document
    prd_markdown = f"""# Product Requirements Document: {req.feature_name}

## 1. Executive Summary
- **Target Users**: {req.target_users}
- **Goals**: {req.goals or "Not specified."}

## 2. Problem Statement & Context
{req.problem_statement}

## 3. User Stories
{req.user_stories or "- No user stories specified."}

## 4. Functional Requirements & Acceptance Criteria
- **Success Metrics**: {req.success_metrics or "Not specified."}
- **Acceptance Criteria**: {req.acceptance_criteria or "Not specified."}

## 5. Risks & Dependencies
- **Dependencies**: {req.dependencies or "None."}
- **Risks**: {req.risks or "None."}
"""

    # Save to SQLite PRD Model
    prd = PRD(
        priority_id=priority.id,
        title=req.feature_name,
        executive_summary=req.goals,
        problem_statement=req.problem_statement,
        objectives=req.goals,
        user_personas=req.target_users,
        user_stories=req.user_stories,
        functional_requirements=req.acceptance_criteria,
        success_metrics=req.success_metrics,
        risks=req.risks,
        open_questions="None"
    )
    db.add(prd)
    db.commit()

    return {
        "title": req.feature_name,
        "content": prd_markdown
    }


@router.post("/api/agents/roadmap")
def roadmap_initiative(req: RoadmapRequest, db: Session = Depends(get_db)):
    """Schedule a roadmap initiative and save to SQLite."""
    # Find/Create PRD target
    cluster = db.query(Cluster).filter(Cluster.cluster_name == req.feature_name).first()
    if not cluster:
        cluster = Cluster(cluster_name=req.feature_name)
        db.add(cluster)
        db.commit()
        db.refresh(cluster)

    priority = db.query(Priority).filter(Priority.cluster_id == cluster.id).first()
    if not priority:
        priority = Priority(cluster_id=cluster.id, priority_level=req.priority)
        db.add(priority)
        db.commit()
        db.refresh(priority)

    prd = db.query(PRD).filter(PRD.priority_id == priority.id).first()
    if not prd:
        prd = PRD(priority_id=priority.id, title=req.feature_name, problem_statement="Created via roadmap scheduler.")
        db.add(prd)
        db.commit()
        db.refresh(prd)

    # Save to Roadmap
    rm = Roadmap(
        prd_id=prd.id,
        title=req.feature_name,
        quarter=req.quarter,
        status=req.status,
        notes=f"Owner: {req.owner} | Progress: {req.progress}%"
    )
    db.add(rm)
    db.commit()

    # Determine recommended quarter
    recommended = req.quarter
    if req.priority == "High":
        recommended = "Q3 2026"
    elif req.priority == "Medium":
        recommended = "Q4 2026"

    return {
        "recommended_quarter": recommended,
        "dependencies": ["Core Platform Authentication", "FastAPI Database Connectors"],
        "quarter": req.quarter,
        "progress": req.progress,
        "feature_name": req.feature_name,
        "priority": req.priority,
        "status": req.status,
        "owner": req.owner
    }


@router.post("/api/orchestrate")
def orchestrate_chat_turn(req: ChatRequest, db: Session = Depends(get_db)):
    """AI Assistant command routing for workspace database entities."""
    prompt = req.prompt.lower()

    if "feedback" in prompt or "theme" in prompt:
        feedback_count = db.query(Feedback).count()
        themes = db.query(Theme).all()
        themes_list = ", ".join(set([t.theme_name for t in themes]))
        return {
            "response": f"I scanned the product database. Currently, there are **{feedback_count} feedback records** indexed. The main customer themes are: **{themes_list or 'none'}**."
        }

    if "feature" in prompt or "priorit" in prompt:
        priorities = db.query(Priority).join(Cluster).all()
        if not priorities:
            return {"response": "The feature prioritization table is empty."}
        p_list = "\n".join([f"- **{p.cluster.cluster_name}**: RICE Score {p.rice_score} ({p.priority_level} Priority)" for p in priorities])
        return {
            "response": f"Here is the priority backlog retrieved from SQLite:\n{p_list}"
        }

    if "roadmap" in prompt:
        roadmaps = db.query(Roadmap).all()
        if not roadmaps:
            return {"response": "No roadmap items currently scheduled."}
        rm_list = "\n".join([f"- **{rm.title}** ({rm.quarter} - Status: {rm.status})" for rm in roadmaps])
        return {
            "response": f"Scheduled roadmap initiatives:\n{rm_list}"
        }

    # Generic PM assistant advice fallback
    return {
        "response": "I am your AI PM Workspace Copilot. I can search feedback trends, calculate RICE scores, compile PRDs, or update roadmaps. Try asking 'What are the main feedback themes?' or 'Show priorities'."
    }
