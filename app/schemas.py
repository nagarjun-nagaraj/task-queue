from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobCreate(BaseModel):
    job_type: str
    payload: dict

class JobResponse(BaseModel):
    id: int
    task_id: str
    job_type: str
    status: str
    result: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
