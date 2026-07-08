from abc import ABC, abstractmethod

from domain.entities.forecast_result import ForecastResult


class ForecastRepository(ABC):

    @abstractmethod
    def save(self, forecast: ForecastResult) -> None:
        raise NotImplementedError
