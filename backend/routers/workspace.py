from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.workspace import (
    create_workspace,
    get_all_workspaces,
    get_workspace_by_id,
    delete_workspace,
)

from database.db import get_db
from schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace"],
)


@router.post("/", response_model=WorkspaceResponse)
def create_new_workspace(
    workspace: WorkspaceCreate,
    db: Session = Depends(get_db),
):
    return create_workspace(db, workspace)


@router.get("/", response_model=list[WorkspaceResponse])
def read_workspaces(
    db: Session = Depends(get_db),
):
    return get_all_workspaces(db)


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def read_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
):
    workspace = get_workspace_by_id(db, workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found",
        )

    return workspace


@router.delete("/{workspace_id}")
def remove_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
):
    workspace = delete_workspace(db, workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found",
        )

    return {
        "message": "Workspace deleted successfully"
    }