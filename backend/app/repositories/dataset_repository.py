from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.dataset import Dataset


class DatasetRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create a new dataset record.
    def create(
        self,
        user_id: UUID,
        uploaded_file_id: UUID,
        name: str,
        row_count: int,
        column_count: int,
        detected_schema: dict,
    ) -> Dataset:
        dataset = Dataset(
            user_id=user_id,
            uploaded_file_id=uploaded_file_id,
            name=name,
            row_count=row_count,
            column_count=column_count,
            detected_schema=detected_schema,
            status="uploaded",
        )
        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)
        return dataset

    # Get a dataset owned by a user.
    def get_owned(self, dataset_id: UUID, user_id: UUID) -> Dataset | None:
        statement = select(Dataset).where(Dataset.id == dataset_id, Dataset.user_id == user_id)
        return self.db.scalar(statement)

    # List datasets owned by a user.
    def list_owned(self, user_id: UUID) -> list[Dataset]:
        statement = select(Dataset).where(Dataset.user_id == user_id).order_by(Dataset.created_at.desc())
        return list(self.db.scalars(statement).all())

    # Update dataset processing status.
    def update_status(self, dataset_id: UUID, status: str) -> Dataset | None:
        dataset = self.db.get(Dataset, dataset_id)

        if dataset is None:
            return None

        dataset.status = status
        self.db.commit()
        self.db.refresh(dataset)
        return dataset

    # Delete a dataset owned by a user.
    def delete_owned(self, dataset_id: UUID, user_id: UUID) -> bool:
        dataset = self.get_owned(dataset_id, user_id)

        if dataset is None:
            return False

        self.db.delete(dataset)
        self.db.commit()
        return True