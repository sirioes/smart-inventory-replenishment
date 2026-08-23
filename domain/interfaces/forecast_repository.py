from abc import ABC, abstractmethod
from typing import List

from domain.entities.forecast_result import ForecastResult


class ForecastRepository(ABC):

    @abstractmethod
    def save(self, forecast: ForecastResult) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_by_product_id(self, product_id: str) -> List[ForecastResult]:
        raise NotImplementedError
