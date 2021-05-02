from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str
    name: str
    description: Optional[str] = None
    location: Optional[str] = None


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
