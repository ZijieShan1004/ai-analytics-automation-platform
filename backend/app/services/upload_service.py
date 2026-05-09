from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.integrations.storage_client import LocalStorageClient
from app.models.user import User
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.job_repository import JobRepository
from app.repositories.uploaded_file_repository import UploadedFileRepository
from app.schemas.dataset import DatasetUploadResponse
from app.tasks.analytics_tasks import process_dataset_job
from app.utils.dataframe_loader import load_dataframe
from app.utils.file_validation import get_file_extension, validate_upload_file


class UploadService:
    def __init__(self, db: Session):
        self.db = db
        self.storage_client = LocalStorageClient()
        self.uploaded_file_repository = UploadedFileRepository(db)
        self.dataset_repository = DatasetRepository(db)
        self.job_repository = JobRepository(db)

    # Store an uploaded dataset and enqueue background processing.
    async def upload_dataset(self, current_user: User, file: UploadFile) -> DatasetUploadResponse:
        content = await file.read()
        validate_upload_file(file.filename, content)

        stored_file = self.storage_client.save_upload(file.filename, content)
        extension = get_file_extension(file.filename)

        uploaded_file = self.uploaded_file_repository.create(
            user_id=current_user.id,
            original_filename=file.filename,
            stored_filename=stored_file["stored_filename"],
            file_path=stored_file["file_path"],
            file_type=extension,
            file_size_bytes=len(content),
            checksum=stored_file["checksum"],
        )

        dataframe = load_dataframe(Path(stored_file["file_path"]))
        detected_schema = {
            "columns": list(dataframe.columns),
            "dtypes": {column: str(dataframe[column].dtype) for column in dataframe.columns},
        }

        dataset = self.dataset_repository.create(
            user_id=current_user.id,
            uploaded_file_id=uploaded_file.id,
            name=file.filename,
            row_count=int(dataframe.shape[0]),
            column_count=int(dataframe.shape[1]),
            detected_schema=detected_schema,
        )

        job = self.job_repository.create(
            user_id=current_user.id,
            dataset_id=dataset.id,
            job_type="full_report",
        )

        process_dataset_job.delay(str(job.id))
        return DatasetUploadResponse(dataset_id=dataset.id, job_id=job.id, status=job.status)