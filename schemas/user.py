from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List, Optional

from db import Project


class CreateUser(BaseModel):
    username: str = Field(..., min_length=4)
    email: EmailStr
    password: str = Field(..., min_length=8)


class ShowUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    avatar: Optional[str] = None
    description: Optional[str] = None
    projects: List[Project]
