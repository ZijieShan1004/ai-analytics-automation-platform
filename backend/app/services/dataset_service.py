from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.models.user import User
from app.repositories.dataset_repository import DatasetRepository


class DatasetService:
    def __init__(self, db: Session):
        self.repository = DatasetRepository(db)

    # List datasets for the current user.
    def list_datasets(self, current_user: User) -> list[Dataset]:
        return self.repository.list_owned(current_user.id)

    # Get one dataset for the current user.
    def get_dataset(self, current_user: User, dataset_id: UUID) -> Dataset:
        dataset = self.repository.get_owned(dataset_id, current_user.id)

        if dataset is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        return dataset

    # Delete one dataset for the current user.
    def delete_dataset(self, current_user: User, dataset_id: UUID) -> dict[str, bool]:
        deleted = self.repository.delete_owned(dataset_id, current_user.id)

        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        return {"deleted": True}