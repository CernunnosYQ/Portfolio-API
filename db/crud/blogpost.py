from sqlalchemy.orm import Session

from db.models.blogpost import Blogpost
from schemas.blogpost import BlogCreate


def create_new_blogpost(blogpost: BlogCreate, db: Session, author_id: int = 1):
    blogpost = Blogpost(**blogpost.__dict__, author_id=author_id)
    db.add(blogpost)
    db.commit()
    db.refresh(blogpost)
    return blogpost


def get_blogpost_by_id(id: int, db: Session):
    blogpost = db.query(Blogpost).filter(Blogpost.id == id).first()
    return blogpost
