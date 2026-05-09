from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class JobResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    job_type: str
    status: str
    progress: int
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)