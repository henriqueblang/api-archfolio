from typing import Optional

from pydantic import BaseModel


class Follower(BaseModel):
    identification: str
