from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.processing_job import ProcessingJob
from app.models.user import User
from app.repositories.job_repository import JobRepository
from app.tasks.analytics_tasks import process_dataset_job


class JobService:
    def __init__(self, db: Session):
        self.repository = JobRepository(db)

    # Get one processing job for the current user.
    def get_job(self, current_user: User, job_id: UUID) -> ProcessingJob:
        job = self.repository.get_owned(job_id, current_user.id)

        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

        return job

    # List processing jobs for the current user.
    def list_jobs(self, current_user: User, status_filter: str | None) -> list[ProcessingJob]:
        return self.repository.list_owned(current_user.id, status_filter)

    # Retry a failed processing job.
    def retry_job(self, current_user: User, job_id: UUID) -> ProcessingJob:
        job = self.get_job(current_user, job_id)

        if job.status not in {"failed", "completed"}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only failed or completed jobs can be retried")

        job.status = "queued"
        job.progress = 0
        job.error_message = None
        self.repository.db.commit()
        self.repository.db.refresh(job)
        process_dataset_job.delay(str(job.id))
        return job