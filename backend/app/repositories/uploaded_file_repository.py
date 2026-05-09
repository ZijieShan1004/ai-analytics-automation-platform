from uuid import UUID

from sqlalchemy.orm import Session

from app.models.uploaded_file import UploadedFile


class UploadedFileRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create a new uploaded file record.
    def create(
        self,
        user_id: UUID,
        original_filename: str,
        stored_filename: str,
        file_path: str,
        file_type: str,
        file_size_bytes: int,
        checksum: str,
    ) -> UploadedFile:
        uploaded_file = UploadedFile(
            user_id=user_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_path=file_path,
            file_type=file_type,
            file_size_bytes=file_size_bytes,
            checksum=checksum,
        )
        self.db.add(uploaded_file)
        self.db.commit()
        self.db.refresh(uploaded_file)
        return uploaded_file