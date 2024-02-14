from db.base import Base
from sqlalchemy import (
    ARRAY,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Project(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    banner = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="projects")
    blog_id = Column(Integer, ForeignKey("blogposts.id"))
    blog = relationship("Blogpost", back_populates="project")
    repository = Column(String, nullable=True)
    container = Column(String, nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    is_active = Column(Boolean, default=False)


class ProjectTest(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    banner = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("usertests.id"))
    author = relationship("UserTest", back_populates="projects")
    blog_id = Column(Integer, ForeignKey("blogposttests.id"))
    blog = relationship("BlogpostTest", back_populates="project")
    repository = Column(String, nullable=True)
    container = Column(String, nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    is_active = Column(Boolean, default=False)
