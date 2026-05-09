from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.forecast import ForecastResultResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


# Get forecast result for a dataset.
@router.get("/{dataset_id}", response_model=ForecastResultResponse)
def get_forecast(
    dataset_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DashboardService(db).get_forecast(current_user, dataset_id)