from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.report import Report
from app.models.user import User
from app.schemas.report import ReportResponse
from app.services.report_service import ReportService

router = APIRouter()


# List reports owned by the current user.
@router.get("", response_model=list[ReportResponse])
def list_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Report]:
    return ReportService(db).list_reports(current_user)


# Get one report owned by the current user.
@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Report:
    return ReportService(db).get_report(current_user, report_id)


# Get the latest report for a dataset.
@router.get("/by-dataset/{dataset_id}", response_model=ReportResponse)
def get_report_by_dataset(
    dataset_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Report:
    return ReportService(db).get_report_by_dataset(current_user, dataset_id)