from sqlalchemy.orm import Session
from .models import (
    Workspace,
    UploadedDocument,
    Feedback,
    Cluster,
    Theme,
    Priority,
    PRD,
    Roadmap,
)

def seed_db(db: Session):
    """Seed sample data if the database is empty."""
    # Check if a workspace already exists
    if db.query(Workspace).first():
        return

    # 1. Create Workspace
    workspace = Workspace(
        id=1,
        name="Default Workspace",
        description="Main product strategy workspace",
    )
    db.add(workspace)
    db.commit()

    # 2. Create Uploaded Document placeholder
    doc = UploadedDocument(
        id=1,
        workspace_id=1,
        file_name="feedback_database_sync",
        file_type="db",
        file_path="database/app.db",
    )
    db.add(doc)
    db.commit()

    # 3. Create Clusters
    core_cluster = Cluster(
        id=1,
        cluster_name="Core Platform Performance",
        summary="User experience pain points relating to slow load times, UI response latency, and navigation friction."
    )
    ai_cluster = Cluster(
        id=2,
        cluster_name="AI Agent Automation",
        summary="Requests and ideas for autonomous agents creating PRDs, drafting feature specs, and prioritizing backlogs automatically."
    )
    api_cluster = Cluster(
        id=3,
        cluster_name="Integrations & API Expansion",
        summary="Developer requests for robust REST APIs, Slack notifications, webhooks, and third-party task tracker synchronizations."
    )
    db.add_all([core_cluster, ai_cluster, api_cluster])
    db.commit()

    # 4. Create Feedbacks
    f1 = Feedback(
        id=1,
        workspace_id=1,
        document_id=1,
        title="Page loads take too long",
        content="The main dashboard navigation is sluggish. Sometimes it takes over 5 seconds to load the feedback trends.",
        source="Intercom",
        customer="Acme Corp"
    )
    f2 = Feedback(
        id=2,
        workspace_id=1,
        document_id=1,
        title="PRD Generation with Markdown",
        content="I love the AI PRD generator! I wish it exported cleanly as Markdown so I can copy it directly into GitHub.",
        source="Zendesk",
        customer="Initech"
    )
    f3 = Feedback(
        id=3,
        workspace_id=1,
        document_id=1,
        title="Slack Integration wanted",
        content="Our team works in Slack. We need a notification when the RICE priority score of a feature is updated.",
        source="Email",
        customer="Globex"
    )
    f4 = Feedback(
        id=4,
        workspace_id=1,
        document_id=1,
        title="Granular permissions",
        content="We need to restrict who can edit the feature prioritization table. Currently everyone has write access.",
        source="Intercom",
        customer="Hooli"
    )
    f5 = Feedback(
        id=5,
        workspace_id=1,
        document_id=1,
        title="Webhook callbacks",
        content="Exposing webhooks for roadmap status updates would allow us to wire updates to Jira automatically.",
        source="API Docs Chat",
        customer="Stark Industries"
    )
    db.add_all([f1, f2, f3, f4, f5])
    db.commit()

    # 5. Create Themes mapping to feedback & clusters
    t1 = Theme(
        id=1,
        feedback_id=1,
        cluster_id=1,
        theme_name="Performance & Speed",
        sentiment="Negative",
        confidence=0.92,
        pain_point="Dashboard load latency",
        intent="Usability improvement"
    )
    t2 = Theme(
        id=2,
        feedback_id=2,
        cluster_id=2,
        theme_name="PRD Automation",
        sentiment="Positive",
        confidence=0.88,
        pain_point="Lack of raw markdown export",
        intent="Feature Request"
    )
    t3 = Theme(
        id=3,
        feedback_id=3,
        cluster_id=3,
        theme_name="Integrations",
        sentiment="Neutral",
        confidence=0.85,
        pain_point="No chat alert support",
        intent="Integration requirement"
    )
    t4 = Theme(
        id=4,
        feedback_id=4,
        cluster_id=1,
        theme_name="UI / UX Refresh",
        sentiment="Negative",
        confidence=0.90,
        pain_point="Lack of team permission scoping",
        intent="Security enhancement"
    )
    t5 = Theme(
        id=5,
        feedback_id=5,
        cluster_id=3,
        theme_name="Integrations",
        sentiment="Neutral",
        confidence=0.94,
        pain_point="Lack of automation webhooks",
        intent="Integration requirement"
    )
    db.add_all([t1, t2, t3, t4, t5])
    db.commit()

    # 6. Create Priority scores (RICE)
    p1 = Priority(
        id=1,
        cluster_id=1,
        rice_score=600.0,
        reach=5000,
        impact=3.0,
        confidence=0.8,
        effort=20.0,
        risk="Low",
        priority_level="Medium",
        scoring_method="RICE"
    )
    p2 = Priority(
        id=2,
        cluster_id=2,
        rice_score=2000.0,
        reach=8000,
        impact=5.0,
        confidence=0.9,
        effort=18.0,
        risk="Medium",
        priority_level="High",
        scoring_method="RICE"
    )
    p3 = Priority(
        id=3,
        cluster_id=3,
        rice_score=360.0,
        reach=3000,
        impact=2.0,
        confidence=0.6,
        effort=10.0,
        risk="High",
        priority_level="Low",
        scoring_method="RICE"
    )
    db.add_all([p1, p2, p3])
    db.commit()

    # 7. Create PRD record
    prd = PRD(
        id=1,
        priority_id=2,
        title="AI PRD Generator",
        executive_summary="Automated PRD document compiler that transforms user problem statements into functional requirements.",
        problem_statement="Users currently write requirements manually, causing design inconsistencies and slow project launches.",
        objectives="Build an AI assistant generating complete PRDs within 10 seconds in Markdown format.",
        user_personas="Product Managers, Engineering Leads",
        user_stories="As a PM, I want to convert feature summaries to PRDs so that engineering understands dependencies.",
        functional_requirements="AI requirement parser, Markdown exporter, customizable goals section.",
        non_functional_requirements="Sub-5 second generation latency, SOC2 compliant secure document endpoints.",
        acceptance_criteria="Generate button outputs valid markdown, includes a copy-to-clipboard button.",
        success_metrics="90%+ reduction in PRD drafting time.",
        risks="Hallucinated requirements or dependencies.",
        open_questions="What integrations are supported first?"
    )
    db.add(prd)
    db.commit()

    # 8. Create Roadmap record
    roadmap = Roadmap(
        id=1,
        prd_id=1,
        title="AI PRD Generator Feature",
        quarter="Q4 2026",
        sprint="Sprint 12",
        milestone="Alpha Launch",
        release_version="v0.4.0",
        status="In Progress",
        notes="Currently working on the LLM parsing optimization pipeline."
    )
    db.add(roadmap)
    db.commit()
