from unittest.mock import MagicMock

from application.use_cases.generate_forecast import GenerateForecastUseCase
from domain.entities.forecast_result import ForecastResult


def test_generate_forecast_calls_strategy_and_saves_result():
    # Arrange: siapkan mock untuk semua dependency, tanpa database sungguhan
    fake_transaction_repo = MagicMock()
    fake_transaction_repo.get_history.return_value = [
        {"quantity_sold": 10, "transaction_date": "2026-07-01"},
        {"quantity_sold": 12, "transaction_date": "2026-07-02"},
    ]

    fake_forecast_repo = MagicMock()

    fake_strategy = MagicMock()
    fake_strategy.predict.return_value = ForecastResult(
        product_id="B1", predicted_demand=11.0, model_version="dummy-v0"
    )

    use_case = GenerateForecastUseCase(
        strategy=fake_strategy,
        transaction_repo=fake_transaction_repo,
        forecast_repo=fake_forecast_repo,
    )

    # Act
    result = use_case.execute(product_id="B1")

    # Assert
    assert result.predicted_demand == 11.0
    fake_transaction_repo.get_history.assert_called_once_with("B1")
    fake_strategy.predict.assert_called_once()
    fake_forecast_repo.save.assert_called_once_with(result)
