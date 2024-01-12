from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional, List


class CreateBlog(BaseModel):
    title: str = str
    slug: str = str
    content: Optional[str] = None
    tags: Optional[List[str]] = None

    @model_validator(mode="before")
    @classmethod
    def check_slug(cls, values):
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values


class ShowBlog(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: Optional[str]
    created_at: datetime
