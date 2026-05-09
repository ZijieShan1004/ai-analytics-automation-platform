import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AIGeneratedSummary(Base):
    __tablename__ = "ai_generated_summaries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id"), index=True)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("processing_jobs.id"), index=True)
    summary_type: Mapped[str] = mapped_column(String(50), default="executive", nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(50), default="v1", nullable=False)
    input_facts: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    generated_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    dataset = relationship("Dataset", back_populates="ai_generated_summaries")
    job = relationship("ProcessingJob", back_populates="ai_generated_summaries")
    reports = relationship("Report", back_populates="ai_summary")