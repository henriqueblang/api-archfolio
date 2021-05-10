from typing import Optional

from pydantic import BaseModel


class Metadata(BaseModel):
    content: Optional[str]
    disposition_order: int


class UpdateMetadata(BaseModel):
    content: Optional[str]
    disposition_order: Optional[int]
