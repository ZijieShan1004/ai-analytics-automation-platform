from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.result_repository import ResultRepository


class DashboardService:
    def __init__(self, db: Session):
        self.dataset_repository = DatasetRepository(db)
        self.result_repository = ResultRepository(db)

    # Get analytics result for a user-owned dataset.
    def get_analytics(self, current_user: User, dataset_id: UUID):
        dataset = self.dataset_repository.get_owned(dataset_id, current_user.id)

        if dataset is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        result = self.result_repository.get_latest_analytics_result(dataset_id)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analytics result not found")

        return result

    # Get chart recommendations for a user-owned dataset.
    def get_charts(self, current_user: User, dataset_id: UUID):
        dataset = self.dataset_repository.get_owned(dataset_id, current_user.id)

        if dataset is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        return self.result_repository.list_chart_recommendations(dataset_id)

    # Get forecast result for a user-owned dataset.
    def get_forecast(self, current_user: User, dataset_id: UUID):
        dataset = self.dataset_repository.get_owned(dataset_id, current_user.id)

        if dataset is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        result = self.result_repository.get_latest_forecast_result(dataset_id)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forecast result not found")

        return result