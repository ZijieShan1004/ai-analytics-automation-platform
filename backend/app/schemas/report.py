from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReportResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    title: str
    report_status: str
    report_payload: dict
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)