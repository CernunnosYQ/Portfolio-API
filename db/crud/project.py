from sqlalchemy.orm import Session

from db.models.project import Project
from schemas.project import ProjectCreate, ProjectUpdate


def create_new_project(project: ProjectCreate, db: Session, author_id: int):
    project = Project(**project.__dict__, author_id=author_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_project_by_id(id: int, db: Session):
    project = db.query(Project).filter(Project.id == id).first()
    return project


def update_project_by_id(id: int, project: ProjectUpdate, db: Session, author_id: int):
    project_in_db = db.query(Project).filter(Project.id == id).first()
    if not project_in_db:
        return {"detail": f"Project with id {id} does not exist"}
    if project_in_db.author_id != author_id:
        return {"detail": "You are trying to edit someone else's project"}
    project_in_db.title = project.title
    project_in_db.description = project.description
    project_in_db.tags = project.tags
    db.add(project_in_db)
    db.commit()
    db.refresh(project_in_db)
    return project_in_db


def delete_project_by_id(id: int, db: Session, author_id: int):
    project_in_db = db.query(Project).filter(Project.id == id)
    if not project_in_db.first():
        return {"detail": f"Project with id {id} does not exist"}
    if project_in_db.first().author_id != author_id:
        return {"detail": "You are trying to delete someone else's project"}
    project_in_db.delete()
    db.commit()
    return {"success": True}
