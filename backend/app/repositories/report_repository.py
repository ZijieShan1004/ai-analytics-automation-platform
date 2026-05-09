from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.report import Report


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create a complete report record.
    def create(
        self,
        user_id: UUID,
        dataset_id: UUID,
        analytics_result_id: UUID,
        forecast_result_id: UUID | None,
        ai_summary_id: UUID,
        title: str,
        report_payload: dict,
    ) -> Report:
        report = Report(
            user_id=user_id,
            dataset_id=dataset_id,
            analytics_result_id=analytics_result_id,
            forecast_result_id=forecast_result_id,
            ai_summary_id=ai_summary_id,
            title=title,
            report_status="ready",
            report_payload=report_payload,
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    # Get a report owned by a user.
    def get_owned(self, report_id: UUID, user_id: UUID) -> Report | None:
        statement = select(Report).where(Report.id == report_id, Report.user_id == user_id)
        return self.db.scalar(statement)

    # Get the latest report for a dataset owned by a user.
    def get_latest_by_dataset(self, dataset_id: UUID, user_id: UUID) -> Report | None:
        statement = (
            select(Report)
            .where(Report.dataset_id == dataset_id, Report.user_id == user_id)
            .order_by(Report.created_at.desc())
        )
        return self.db.scalar(statement)

    # List reports owned by a user.
    def list_owned(self, user_id: UUID) -> list[Report]:
        statement = select(Report).where(Report.user_id == user_id).order_by(Report.created_at.desc())
        return list(self.db.scalars(statement).all())