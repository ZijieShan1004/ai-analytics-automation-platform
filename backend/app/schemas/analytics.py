from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnalyticsResultResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    numeric_columns: list
    categorical_columns: list
    datetime_columns: list
    missing_value_summary: dict
    outlier_summary: dict
    correlation_matrix: dict
    kpi_summary: dict
    trend_summary: dict
    anomaly_summary: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChartRecommendationResponse(BaseModel):
    id: UUID
    chart_type: str
    title: str
    x_column: str | None
    y_column: str | None
    group_by_column: str | None
    aggregation: str | None
    confidence_score: float
    reason: str
    chart_payload: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)