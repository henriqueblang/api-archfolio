from typing import Optional

from pydantic import BaseModel


class Comment(BaseModel):
    user_id: int
    content: str
