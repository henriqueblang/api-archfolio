from typing import List, Optional

from pydantic import BaseModel


class Post(BaseModel):
    author: int
    title: str
    description: str
    tags: List[str]


class UpdatePost(BaseModel):
    title: str
    description: str
    tags: List[str]
    views: int
