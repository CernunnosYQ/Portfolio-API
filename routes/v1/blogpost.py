from fastapi import APIRouter, Depends, HTTPException, status
from schemas.blogpost import BlogCreate, BlogShow, BlogUpdate
from sqlalchemy.orm import Session

from db.session import get_db
from db.crud.blogpost import (
    create_new_blogpost,
    get_blogpost_by_id,
    update_blogpost_by_id,
    delete_blogpost_by_id,
)
from db.models.user import User

from routes.v1.auth import get_current_user

router = APIRouter()


@router.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_blogpost(
    blog: BlogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    blogpost = create_new_blogpost(blogpost=blog, db=db, author_id=current_user.id)
    return blogpost


@router.get("/blogs/{id}", response_model=BlogShow)
def get_blogpost(id: int, db: Session = Depends(get_db)):
    blogpost = get_blogpost_by_id(id=id, db=db)
    if not blogpost:
        raise HTTPException(
            detail=f"Blogpost with ID {id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return BlogShow(**blogpost.__dict__)


@router.put("/blogs/{id}", status_code=status.HTTP_200_OK)
def update_blogpost(
    id: int,
    blog: BlogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    blogpost = update_blogpost_by_id(id=id, blog=blog, db=db, author_id=current_user.id)
    if isinstance(blogpost, dict):
        raise HTTPException(
            detail=blogpost.get("detail"), status_code=status.HTTP_404_NOT_FOUND
        )
    return BlogShow(**blogpost.__dict__)


@router.delete("/blogs/{id}", status_code=status.HTTP_200_OK)
def delete_blogpost(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = delete_blogpost_by_id(id=id, db=db, author_id=current_user.id)
    if not message.get("success"):
        raise HTTPException(
            detail=message.get("detail"), status_code=status.HTTP_404_NOT_FOUND
        )
    return {"message": f"Successfully deleted blog with id {id}"}
