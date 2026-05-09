from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.processing_job import ProcessingJob
from app.models.user import User
from app.schemas.job import JobResponse
from app.services.job_service import JobService

router = APIRouter()


# List processing jobs owned by the current user.
@router.get("", response_model=list[JobResponse])
def list_jobs(
    status: str | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ProcessingJob]:
    return JobService(db).list_jobs(current_user, status)


# Get a processing job owned by the current user.
@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProcessingJob:
    return JobService(db).get_job(current_user, job_id)


# Retry a completed or failed processing job.
@router.post("/{job_id}/retry", response_model=JobResponse)
def retry_job(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProcessingJob:
    return JobService(db).retry_job(current_user, job_id)