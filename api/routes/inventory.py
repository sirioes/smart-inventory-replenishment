from fastapi import APIRouter, Depends, HTTPException, status
from api.dependencies import get_facade
from api.schemas.product_schema import ReorderRecommendationResponse
from application.inventory_service_facade import InventoryServiceFacade

router = APIRouter(prefix="/products", tags=["inventory"])

@router.post(
    "/{product_id}/process",
    response_model=ReorderRecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Run the full inventory evaluation cycle for a product",
)
def process_product(
    product_id: str,
    facade: InventoryServiceFacade = Depends(get_facade),
) -> ReorderRecommendationResponse:
    try:
        recommendation = facade.process_product(product_id=product_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    return ReorderRecommendationResponse.model_validate(recommendation)
