from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional, List


class CreatePost(BaseModel):
    title: str = str
    description: Optional[str] = None
    banner: Optional[str] = None
    blog_id = Optional[int]
    repository = Optional[HttpUrl] = None
    container = Optional[HttpUrl] = None
    tags = Optional[List[str]]


class ShowPost(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = str
    description: Optional[str]
    banner: Optional[str]
    blog_id = Optional[int]
    repository = Optional[HttpUrl]
    container = Optional[HttpUrl]
    tags = List[str]
