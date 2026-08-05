from sqlalchemy.orm import Session

from ..database.models import Workspace
from ..schemas.workspace import WorkspaceCreate


def create_workspace(db: Session, workspace: WorkspaceCreate):
    db_workspace = Workspace(
        name=workspace.name,
        description=workspace.description,
    )

    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)

    return db_workspace


def get_all_workspaces(db: Session):
    return db.query(Workspace).all()


def get_workspace_by_id(db: Session, workspace_id: int):
    return (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )


def delete_workspace(db: Session, workspace_id: int):
    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )

    if workspace is None:
        return None

    db.delete(workspace)
    db.commit()

    return workspace