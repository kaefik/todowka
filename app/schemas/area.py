from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AreaCreate(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None


class AreaResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    color: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
