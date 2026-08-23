from datetime import date
from unittest.mock import MagicMock

import pytest

from application.use_cases.get_forecast_history import GetForecastHistoryUseCase
from domain.entities.forecast_result import ForecastResult
from domain.entities.product import Product


def test_get_forecast_history_returns_forecasts_for_product():
    # Arrange
    product_repo = MagicMock()
    product_repo.get_by_id.return_value = Product(
        id="P1", sku="SKU-1", name="Widget", lead_time_days=3
    )

    forecast_repo = MagicMock()
    forecast_repo.list_by_product_id.return_value = [
        ForecastResult(
            product_id="P1",
            predicted_demand=10.0,
            model_version="xgboost-v1",
            forecast_date=date(2026, 8, 1),
        ),
        ForecastResult(
            product_id="P1",
            predicted_demand=12.5,
            model_version="xgboost-v1",
            forecast_date=date(2026, 8, 8),
        ),
    ]

    use_case = GetForecastHistoryUseCase(
        product_repo=product_repo, forecast_repo=forecast_repo
    )

    # Act
    result = use_case.execute(product_id="P1")

    # Assert
    assert len(result) == 2
    assert result[0].predicted_demand == 10.0
    assert result[1].predicted_demand == 12.5
    product_repo.get_by_id.assert_called_once_with("P1")
    forecast_repo.list_by_product_id.assert_called_once_with("P1")


def test_get_forecast_history_raises_when_product_missing():
    product_repo = MagicMock()
    product_repo.get_by_id.side_effect = ValueError(
        "Product dengan id=missing-id tidak ditemukan"
    )
    forecast_repo = MagicMock()

    use_case = GetForecastHistoryUseCase(
        product_repo=product_repo, forecast_repo=forecast_repo
    )

    with pytest.raises(ValueError):
        use_case.execute(product_id="missing-id")

    # Repository forecast nggak boleh kepanggil kalau produknya aja nggak ada
    forecast_repo.list_by_product_id.assert_not_called()
