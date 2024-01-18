from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional, List


class BlogCreate(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None
    tags: Optional[List[str]] = None

    @model_validator(mode="before")
    @classmethod
    def check_slug(cls, values):
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values


class BlogShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: Optional[str]
    created_at: datetime


class BlogUpdate(BlogCreate):
    pass
