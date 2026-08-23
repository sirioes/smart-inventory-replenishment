from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from api.dependencies import get_forecast_history_use_case, get_forecast_use_case
from api.schemas.forecast_schema import ForecastResponse
from application.use_cases.generate_forecast import GenerateForecastUseCase
from application.use_cases.get_forecast_history import GetForecastHistoryUseCase

router = APIRouter(prefix="/products", tags=["forecasts"])

@router.post(
    "/{product_id}/forecast",
    response_model=ForecastResponse,
    status_code=status.HTTP_200_OK,
    summary="Trigger an on-demand demand forecast for a product",
)
def trigger_forecast(
    product_id: str,
    use_case: GenerateForecastUseCase = Depends(get_forecast_use_case),
) -> ForecastResponse:
    try:
        forecast = use_case.execute(product_id=product_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    return ForecastResponse.model_validate(forecast)

@router.get(
    "/{product_id}/forecasts",
    response_model=List[ForecastResponse],
    summary="List historical forecasts generated for a product, oldest first",
)
def list_forecast_history(
    product_id: str,
    use_case: GetForecastHistoryUseCase = Depends(get_forecast_history_use_case),
) -> List[ForecastResponse]:
    try:
        history = use_case.execute(product_id=product_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    return [ForecastResponse.model_validate(item) for item in history]
