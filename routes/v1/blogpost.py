from fastapi import APIRouter, Depends, HTTPException, status
from schemas.blogpost import BlogCreate, BlogShow
from sqlalchemy.orm import Session

from db.session import get_db
from db.crud.blogpost import create_new_blogpost, get_blogpost_by_id

router = APIRouter()


@router.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_blogpost(
    blog: BlogCreate, db: Session = Depends(get_db), author_id: int = 1
):
    blogpost = create_new_blogpost(blogpost=blog, db=db, author_id=author_id)
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
