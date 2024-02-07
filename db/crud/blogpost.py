from sqlalchemy.orm import Session

from db.models.blogpost import Blogpost
from schemas.blogpost import BlogCreate, BlogUpdate


def create_new_blogpost(blogpost: BlogCreate, db: Session, author_id: int):
    blogpost = Blogpost(**blogpost.__dict__, author_id=author_id)
    db.add(blogpost)
    db.commit()
    db.refresh(blogpost)
    return blogpost


def get_blogpost_by_id(id: int, db: Session):
    blogpost = db.query(Blogpost).filter(Blogpost.id == id).first()
    return blogpost


def get_blogpost_by_slug(slug: int, db: Session):
    blogpost = db.query(Blogpost).filter(Blogpost.slug == slug).first()
    return blogpost


def get_blogpost_all(db: Session):
    all_blogpost = db.query(Blogpost).all()
    return all_blogpost


def update_blogpost_by_id(id: int, blog: BlogUpdate, db: Session, author_id: int):
    blog_in_db = db.query(Blogpost).filter(Blogpost.id == id).first()
    if not blog_in_db:
        return {"detail": f"Blogpost with id {id} does not exist"}
    if blog_in_db.author_id != author_id:
        return {"detail": "You are trying to edit someone else's post"}
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    blog_in_db.tags = blog.tags
    db.add(blog_in_db)
    db.commit()
    db.refresh(blog_in_db)
    return blog_in_db


def delete_blogpost_by_id(id: int, db: Session, author_id: int):
    blog_in_db = db.query(Blogpost).filter(Blogpost.id == id)
    if not blog_in_db.first():
        return {"detail": f"Blogpost with id {id} does not exist"}
    if blog_in_db.first().author_id != author_id:
        return {"detail": "You are trying to delete someone else's post"}
    blog_in_db.delete()
    db.commit()
    return {"success": True}
