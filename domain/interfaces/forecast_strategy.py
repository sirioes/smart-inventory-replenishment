from abc import ABC, abstractmethod
from typing import Any, Dict, List

from domain.entities.forecast_result import ForecastResult


class ForecastStrategy(ABC):

    @abstractmethod
    def predict(
        self, product_id: str, historical_data: List[Dict[str, Any]]
    ) -> ForecastResult:
        raise NotImplementedError
