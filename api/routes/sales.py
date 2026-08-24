from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_sales_history_use_case
from api.schemas.sales_schema import SalesHistoryItem
from application.use_cases.get_sales_history import GetSalesHistoryUseCase

router = APIRouter(prefix="/products", tags=["sales"])

@router.get(
    "/{product_id}/sales-history",
    response_model=List[SalesHistoryItem],
    summary="List historical sales transactions for a product, oldest first",
)
def list_sales_history(
    product_id: str,
    use_case: GetSalesHistoryUseCase = Depends(get_sales_history_use_case),
) -> List[SalesHistoryItem]:
    try:
        history = use_case.execute(product_id=product_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    return [SalesHistoryItem.model_validate(item) for item in history]
