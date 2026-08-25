from typing import List

from fastapi import APIRouter, Depends

from api.dependencies import get_alerts_feed_use_case
from api.schemas.alert_schema import AlertFeedItem
from application.use_cases.get_alerts_feed import GetAlertsFeedUseCase

router = APIRouter(tags=["alerts"])

@router.get(
    "/alerts",
    response_model=List[AlertFeedItem],
    summary="List recent alerts with product context, most recent first",
)
def list_alerts(
    limit: int = 50,
    use_case: GetAlertsFeedUseCase = Depends(get_alerts_feed_use_case),
) -> List[AlertFeedItem]:
    items = use_case.execute(limit=limit)
    return [AlertFeedItem.model_validate(item) for item in items]
