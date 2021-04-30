from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    name: str
    description: str
    location: str


class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
