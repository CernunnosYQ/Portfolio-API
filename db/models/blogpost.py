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


class Blogpost(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    banner = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="blogs")
    tags = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    project = relationship("Project", uselist=False, back_populates="blog")
    is_active = Column(Boolean, default=False)
