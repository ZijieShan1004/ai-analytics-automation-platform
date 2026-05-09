from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.analytics import AnalyticsResultResponse, ChartRecommendationResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


# Get analytics results for a dataset.
@router.get("/{dataset_id}", response_model=AnalyticsResultResponse)
def get_analytics(
    dataset_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DashboardService(db).get_analytics(current_user, dataset_id)


# Get chart recommendations for a dataset.
@router.get("/{dataset_id}/charts", response_model=list[ChartRecommendationResponse])
def get_charts(
    dataset_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DashboardService(db).get_charts(current_user, dataset_id)