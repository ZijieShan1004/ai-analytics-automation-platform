from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.report import Report
from app.models.user import User
from app.repositories.report_repository import ReportRepository


class ReportService:
    def __init__(self, db: Session):
        self.repository = ReportRepository(db)

    # List reports for the current user.
    def list_reports(self, current_user: User) -> list[Report]:
        return self.repository.list_owned(current_user.id)

    # Get one report for the current user.
    def get_report(self, current_user: User, report_id: UUID) -> Report:
        report = self.repository.get_owned(report_id, current_user.id)

        if report is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

        return report

    # Get the latest report for a dataset.
    def get_report_by_dataset(self, current_user: User, dataset_id: UUID) -> Report:
        report = self.repository.get_latest_by_dataset(dataset_id, current_user.id)

        if report is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

        return report