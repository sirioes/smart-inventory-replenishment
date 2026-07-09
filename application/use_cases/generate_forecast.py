from domain.entities.forecast_result import ForecastResult
from domain.interfaces.forecast_repository import ForecastRepository
from domain.interfaces.forecast_strategy import ForecastStrategy
from domain.interfaces.transaction_repository import TransactionRepository


class GenerateForecastUseCase:

    def __init__(
        self,
        strategy: ForecastStrategy,
        transaction_repo: TransactionRepository,
        forecast_repo: ForecastRepository,
    ) -> None:
        self.strategy = strategy
        self.transaction_repo = transaction_repo
        self.forecast_repo = forecast_repo

    def execute(self, product_id: str) -> ForecastResult:
        historical_data = self.transaction_repo.get_history(product_id)
        forecast = self.strategy.predict(product_id, historical_data)
        self.forecast_repo.save(forecast)
        return forecast
