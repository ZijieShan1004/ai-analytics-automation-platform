from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.dataset import Dataset
from app.models.user import User
from app.schemas.dataset import DatasetResponse, DatasetUploadResponse
from app.services.dataset_service import DatasetService
from app.services.upload_service import UploadService

router = APIRouter()


# Upload a dataset and start asynchronous processing.
@router.post("/upload", response_model=DatasetUploadResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DatasetUploadResponse:
    return await UploadService(db).upload_dataset(current_user, file)


# List datasets owned by the current user.
@router.get("", response_model=list[DatasetResponse])
def list_datasets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Dataset]:
    return DatasetService(db).list_datasets(current_user)


# Get a dataset owned by the current user.
@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(
    dataset_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dataset:
    return DatasetService(db).get_dataset(current_user, dataset_id)


# Delete a dataset owned by the current user.
@router.delete("/{dataset_id}")
def delete_dataset(
    dataset_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, bool]:
    return DatasetService(db).delete_dataset(current_user, dataset_id)