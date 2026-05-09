import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ForecastResult(Base):
    __tablename__ = "forecast_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id"), index=True)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("processing_jobs.id"), index=True)
    datetime_column: Mapped[str | None] = mapped_column(String(255), nullable=True)
    target_column: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model_type: Mapped[str] = mapped_column(String(50), default="none", nullable=False)
    forecast_horizon: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    metrics: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    forecast_values: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    confidence_intervals: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    dataset = relationship("Dataset", back_populates="forecast_results")
    job = relationship("ProcessingJob", back_populates="forecast_results")
    reports = relationship("Report", back_populates="forecast_result")