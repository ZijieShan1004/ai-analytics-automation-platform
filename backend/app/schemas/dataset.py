from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DatasetResponse(BaseModel):
    id: UUID
    name: str
    row_count: int
    column_count: int
    detected_schema: dict
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DatasetUploadResponse(BaseModel):
    dataset_id: UUID
    job_id: UUID
    status: str