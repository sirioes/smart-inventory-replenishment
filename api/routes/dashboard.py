from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from api.dependencies import get_dashboard_use_case
from api.schemas.dashboard_schema import DashboardResponse, ProductDashboardItem
from application.use_cases.get_dashboard_data import GetDashboardDataUseCase

router = APIRouter(tags=["dashboard"])

@router.get(
    "/dashboard",
    response_model=DashboardResponse,
    summary="Aggregate product, inventory, and reorder data for the frontend dashboard",
)
def get_dashboard(
    use_case: GetDashboardDataUseCase = Depends(get_dashboard_use_case),
) -> DashboardResponse:
    rows = use_case.execute()
    return DashboardResponse(
        products=[ProductDashboardItem.model_validate(row) for row in rows],
        generated_at=datetime.now(timezone.utc),
    )
