import os
import sys
import uuid
from typing import Dict

import pandas as pd
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.database.db import SessionLocal
from backend.database.models import (
    Cluster,
    Feedback,
    Priority,
    Theme,
    UploadedDocument,
    Workspace,
)

XLSX_PATH = os.path.join(PROJECT_ROOT, "AI_PM_Copilot__Multi_Stakeholder_Dataset.xlsx")


def get_or_create_workspace(db: Session) -> Workspace:
    workspace = db.query(Workspace).first()
    if not workspace:
        workspace = Workspace(
            name="Default Workspace",
            description="Workspace imported from Excel dataset.",
        )
        db.add(workspace)
        db.commit()
        db.refresh(workspace)
    return workspace


def get_or_create_uploaded_document(db: Session) -> UploadedDocument:
    document = db.query(UploadedDocument).filter_by(file_name=os.path.basename(XLSX_PATH)).first()
    if not document:
        workspace = get_or_create_workspace(db)
        document = UploadedDocument(
            workspace_id=workspace.id,
            file_name=os.path.basename(XLSX_PATH),
            file_type="xlsx",
            file_path=XLSX_PATH,
        )
        db.add(document)
        db.commit()
        db.refresh(document)
    return document


def get_or_create_cluster(db: Session, cluster_name: str, summary: str = "Imported from Excel dataset.") -> Cluster:
    cluster = db.query(Cluster).filter(Cluster.cluster_name == cluster_name).first()
    if not cluster:
        cluster = Cluster(cluster_name=cluster_name, summary=summary)
        db.add(cluster)
        db.commit()
        db.refresh(cluster)
    return cluster


def import_feedback(db: Session, workspace: Workspace, document: UploadedDocument) -> int:
    feedback_df = pd.read_excel(XLSX_PATH, sheet_name="Users_Feedback")
    if feedback_df.empty:
        return 0

    theme_cache: Dict[str, Cluster] = {}
    imported_count = 0
    for _, row in feedback_df.iterrows():
        feedback_id = str(row.get("feedback_id", uuid.uuid4()))
        title = str(row.get("feature_request", ""))[:120] if row.get("feature_request") is not None else str(row.get("feedback_text", ""))[:120]
        content = str(row.get("feedback_text", "")).strip()
        source = str(row.get("source", "Excel"))
        customer = str(row.get("user_name", "Excel User"))

        if not content:
            continue

        feedback = Feedback(
            workspace_id=workspace.id,
            document_id=document.id,
            title=title,
            content=content,
            source=source,
            customer=customer,
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        imported_count += 1

        theme_name = str(row.get("theme", "Unknown")).strip() or "Unknown"
        cluster = theme_cache.get(theme_name)
        if not cluster:
            cluster = get_or_create_cluster(db, cluster_name=theme_name)
            theme_cache[theme_name] = cluster

        try:
            confidence = float(row.get("confidence_score", 0) or 0)
        except Exception:
            confidence = 0.0

        theme = Theme(
            feedback_id=feedback.id,
            cluster_id=cluster.id,
            theme_name=theme_name,
            sentiment=str(row.get("sentiment", "Unknown")),
            confidence=confidence,
            pain_point=str(row.get("feature_request", ""))[:255],
            intent=str(row.get("priority", ""))[:255],
        )
        db.add(theme)
        db.commit()

    return imported_count


def import_priorities(db: Session) -> int:
    priorities_df = pd.read_excel(XLSX_PATH, sheet_name="Feature_Initiatives")
    if priorities_df.empty:
        return 0

    imported_count = 0
    for _, row in priorities_df.iterrows():
        feature_name = str(row.get("feature_name", "Unnamed Feature")).strip()
        if not feature_name:
            continue

        cluster = get_or_create_cluster(db, cluster_name=feature_name, summary=str(row.get("theme", "")))

        try:
            rice_score = float(row.get("rice_score", 0) or 0)
        except Exception:
            rice_score = 0.0

        try:
            reach = int(row.get("reach", 0) or 0)
        except Exception:
            reach = 0

        try:
            impact = float(row.get("impact", 0) or 0)
        except Exception:
            impact = 0.0

        try:
            confidence = float(row.get("confidence", 0) or 0)
        except Exception:
            confidence = 0.0

        try:
            effort = float(row.get("effort", 0) or 0)
        except Exception:
            effort = 0.0

        status = str(row.get("initiative_status", "")).strip()
        if status.lower() in {"approved", "in progress", "live"}:
            priority_level = "High"
        elif status.lower() in {"candidate", "planned"}:
            priority_level = "Medium"
        else:
            priority_level = "Low"

        existing = db.query(Priority).filter(Priority.cluster_id == cluster.id).first()
        if existing:
            existing.rice_score = rice_score
            existing.reach = reach
            existing.impact = impact
            existing.confidence = confidence
            existing.effort = effort
            existing.priority_level = priority_level
            existing.scoring_method = "RICE"
            db.commit()
        else:
            priority = Priority(
                cluster_id=cluster.id,
                rice_score=rice_score,
                reach=reach,
                impact=impact,
                confidence=confidence,
                effort=effort,
                risk=str(row.get("value_driver", ""))[:100],
                priority_level=priority_level,
                scoring_method="RICE",
            )
            db.add(priority)
            db.commit()
            imported_count += 1

    return imported_count


def main() -> int:
    if not os.path.exists(XLSX_PATH):
        print(f"Excel file not found: {XLSX_PATH}")
        return 1

    db = SessionLocal()
    try:
        workspace = get_or_create_workspace(db)
        document = get_or_create_uploaded_document(db)

        print(f"Importing data from: {XLSX_PATH}")
        feedback_count = import_feedback(db, workspace, document)
        priority_count = import_priorities(db)

        print(f"Imported {feedback_count} feedback rows.")
        print(f"Imported/updated {priority_count} priority rows.")
    finally:
        db.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
