from typing import Optional

from pydantic import BaseModel


class Favorite(BaseModel):
    user_id: int
