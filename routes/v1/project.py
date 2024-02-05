from fastapi import APIRouter, Depends, HTTPException, status
from schemas.project import ProjectCreate, ProjectShow, ProjectUpdate
from sqlalchemy.orm import Session

from db.session import get_db
from db.crud.project import (
    create_new_project,
    get_project_by_id,
    update_project_by_id,
    delete_project_by_id,
)
from db.models.user import User

from routes.v1.auth import get_current_user

router = APIRouter()


@router.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = create_new_project(project=project, db=db, author_id=current_user.id)
    return project


@router.get("/project/{id}", response_model=ProjectShow)
def get_project(
    id: int,
    db: Session = Depends(get_db),
):
    project = get_project_by_id(id=id, db=db)
    if not project:
        raise HTTPException(
            detail=f"Project with ID {id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return ProjectShow(**project.__dict__)


@router.put("/project/{id}", response_model=ProjectShow)
def update_project(
    id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = update_project_by_id(
        id=id, project=project, db=db, author_id=current_user.id
    )
    if isinstance(project, dict):
        raise HTTPException(
            detail=project.get("detail"), status_code=status.HTTP_404_NOT_FOUND
        )
    return ProjectShow(**project.__dict__)


@router.delete("/project/{id}", status_code=status.HTTP_200_OK)
def delete_blogpost(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = delete_project_by_id(id=id, db=db, author_id=current_user.id)
    if not message.get("success"):
        raise HTTPException(
            detail=message.get("detail"), status_code=status.HTTP_404_NOT_FOUND
        )
    return {"message": f"Successfully deleted project with id {id}"}
