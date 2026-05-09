from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.processing_job import ProcessingJob


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create a new processing job.
    def create(self, user_id: UUID, dataset_id: UUID, job_type: str = "full_report") -> ProcessingJob:
        job = ProcessingJob(user_id=user_id, dataset_id=dataset_id, job_type=job_type, status="queued")
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    # Get a job by id.
    def get_by_id(self, job_id: UUID) -> ProcessingJob | None:
        return self.db.get(ProcessingJob, job_id)

    # Get a job owned by a user.
    def get_owned(self, job_id: UUID, user_id: UUID) -> ProcessingJob | None:
        statement = select(ProcessingJob).where(
            ProcessingJob.id == job_id,
            ProcessingJob.user_id == user_id,
        )
        return self.db.scalar(statement)

    # List jobs owned by a user.
    def list_owned(self, user_id: UUID, status: str | None = None) -> list[ProcessingJob]:
        statement = select(ProcessingJob).where(ProcessingJob.user_id == user_id)

        if status is not None:
            statement = statement.where(ProcessingJob.status == status)

        statement = statement.order_by(ProcessingJob.created_at.desc())
        return list(self.db.scalars(statement).all())

    # Mark a job as running.
    def mark_running(self, job_id: UUID, progress: int = 5) -> ProcessingJob | None:
        job = self.get_by_id(job_id)

        if job is None:
            return None

        job.status = "running"
        job.progress = progress
        job.started_at = datetime.utcnow()
        job.error_message = None
        self.db.commit()
        self.db.refresh(job)
        return job

    # Update job progress.
    def update_progress(self, job_id: UUID, progress: int) -> ProcessingJob | None:
        job = self.get_by_id(job_id)

        if job is None:
            return None

        job.progress = progress
        self.db.commit()
        self.db.refresh(job)
        return job

    # Mark a job as completed.
    def mark_completed(self, job_id: UUID) -> ProcessingJob | None:
        job = self.get_by_id(job_id)

        if job is None:
            return None

        job.status = "completed"
        job.progress = 100
        job.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(job)
        return job

    # Mark a job as failed.
    def mark_failed(self, job_id: UUID, error_message: str) -> ProcessingJob | None:
        job = self.get_by_id(job_id)

        if job is None:
            return None

        job.status = "failed"
        job.error_message = error_message
        job.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(job)
        return job