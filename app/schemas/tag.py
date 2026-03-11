from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TagCreate(BaseModel):
    name: str
    color: Optional[str] = None


class TagResponse(BaseModel):
    id: int
    name: str
    color: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
