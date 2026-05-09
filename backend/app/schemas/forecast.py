from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ForecastResultResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    datetime_column: str | None
    target_column: str | None
    model_type: str
    forecast_horizon: int
    metrics: dict
    forecast_values: list
    confidence_intervals: list
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)