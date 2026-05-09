import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ChartRecommendation(Base):
    __tablename__ = "chart_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id"), index=True)
    analytics_result_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analytics_results.id"),
        index=True,
    )
    chart_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    x_column: Mapped[str | None] = mapped_column(String(255), nullable=True)
    y_column: Mapped[str | None] = mapped_column(String(255), nullable=True)
    group_by_column: Mapped[str | None] = mapped_column(String(255), nullable=True)
    aggregation: Mapped[str | None] = mapped_column(String(50), nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    chart_payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    dataset = relationship("Dataset", back_populates="chart_recommendations")
    analytics_result = relationship("AnalyticsResult", back_populates="chart_recommendations")