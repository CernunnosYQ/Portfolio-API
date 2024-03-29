from db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    avatar = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    date_joined = Column(DateTime, nullable=False, default=func.now())
    last_update = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    blogs = relationship("Blogpost", back_populates="author")
    projects = relationship("Project", back_populates="author")


class UserTest(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    avatar = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    date_joined = Column(DateTime, nullable=False, default=func.now())
    last_update = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    blogs = relationship("BlogpostTest", back_populates="author")
    projects = relationship("ProjectTest", back_populates="author")
