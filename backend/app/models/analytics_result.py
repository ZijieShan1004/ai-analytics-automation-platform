import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AnalyticsResult(Base):
    __tablename__ = "analytics_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id"), index=True)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("processing_jobs.id"), index=True)
    numeric_columns: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    categorical_columns: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    datetime_columns: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    missing_value_summary: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    outlier_summary: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    correlation_matrix: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    kpi_summary: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    trend_summary: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    anomaly_summary: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    dataset = relationship("Dataset", back_populates="analytics_results")
    job = relationship("ProcessingJob", back_populates="analytics_results")
    chart_recommendations = relationship("ChartRecommendation", back_populates="analytics_result")
    reports = relationship("Report", back_populates="analytics_result")