from typing import Optional

from pydantic import BaseModel


class Like(BaseModel):
    user_id: int
