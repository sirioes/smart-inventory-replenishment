from typing import List

from domain.entities.forecast_result import ForecastResult
from domain.interfaces.forecast_repository import ForecastRepository
from domain.interfaces.product_repository import ProductRepository


class GetForecastHistoryUseCase:

    def __init__(
        self,
        product_repo: ProductRepository,
        forecast_repo: ForecastRepository,
    ) -> None:
        self.product_repo = product_repo
        self.forecast_repo = forecast_repo

    def execute(self, product_id: str) -> List[ForecastResult]:
        self.product_repo.get_by_id(product_id)  # raises ValueError if not found
        return self.forecast_repo.list_by_product_id(product_id)
