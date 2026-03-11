from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ContextCreate(BaseModel):
    name: str
    icon: Optional[str] = None
    color: Optional[str] = None


class ContextResponse(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    color: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
