from unittest.mock import MagicMock

from application.inventory_service_facade import InventoryServiceFacade
from domain.entities.forecast_result import ForecastResult
from domain.entities.reorder_recommendation import ReorderRecommendation


def test_process_product_dispatches_alert_when_restock_needed():
    forecast = ForecastResult(
        product_id="B1", predicted_demand=8.0, model_version="dummy-v0"
    )
    recommendation = ReorderRecommendation(
        product_id="B1", reorder_point=20.0, recommended_qty=15, needs_restock=True
    )

    fake_forecast_use_case = MagicMock()
    fake_forecast_use_case.execute.return_value = forecast

    fake_reorder_use_case = MagicMock()
    fake_reorder_use_case.execute.return_value = recommendation

    fake_alert_use_case = MagicMock()

    facade = InventoryServiceFacade(
        forecast_use_case=fake_forecast_use_case,
        reorder_use_case=fake_reorder_use_case,
        alert_use_case=fake_alert_use_case,
    )

    result = facade.process_product(product_id="B1")

    assert result is recommendation
    fake_forecast_use_case.execute.assert_called_once_with(product_id="B1")
    fake_reorder_use_case.execute.assert_called_once_with(
        product_id="B1", forecast=forecast
    )
    fake_alert_use_case.execute.assert_called_once_with(recommendation=recommendation)


def test_process_product_skips_alert_when_restock_not_needed():
    forecast = ForecastResult(
        product_id="B2", predicted_demand=2.0, model_version="dummy-v0"
    )
    recommendation = ReorderRecommendation(
        product_id="B2", reorder_point=5.0, recommended_qty=0, needs_restock=False
    )

    fake_forecast_use_case = MagicMock()
    fake_forecast_use_case.execute.return_value = forecast

    fake_reorder_use_case = MagicMock()
    fake_reorder_use_case.execute.return_value = recommendation

    fake_alert_use_case = MagicMock()

    facade = InventoryServiceFacade(
        forecast_use_case=fake_forecast_use_case,
        reorder_use_case=fake_reorder_use_case,
        alert_use_case=fake_alert_use_case,
    )

    result = facade.process_product(product_id="B2")

    assert result is recommendation
    fake_alert_use_case.execute.assert_not_called()
