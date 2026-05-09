import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    uploaded_file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("uploaded_files.id"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    row_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    column_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    detected_schema: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="uploaded", index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = relationship("User", back_populates="datasets")
    uploaded_file = relationship("UploadedFile", back_populates="dataset")
    processing_jobs = relationship("ProcessingJob", back_populates="dataset", cascade="all, delete-orphan")
    analytics_results = relationship("AnalyticsResult", back_populates="dataset", cascade="all, delete-orphan")
    chart_recommendations = relationship(
        "ChartRecommendation",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )
    forecast_results = relationship("ForecastResult", back_populates="dataset", cascade="all, delete-orphan")
    ai_generated_summaries = relationship(
        "AIGeneratedSummary",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )
    reports = relationship("Report", back_populates="dataset", cascade="all, delete-orphan")