from unittest.mock import MagicMock

from application.use_cases.calculate_reorder_point import CalculateReorderPointUseCase
from domain.entities.forecast_result import ForecastResult
from domain.entities.inventory_item import InventoryItem
from domain.entities.product import Product


def test_needs_restock_when_stock_below_reorder_point():
    fake_product_repo = MagicMock()
    fake_product_repo.get_by_id.return_value = Product(
        id="B1", sku="SKU-1", name="Baju Barong", lead_time_days=7
    )

    fake_inventory_repo = MagicMock()
    fake_inventory_repo.get_by_product_id.return_value = InventoryItem(
        product_id="B1", current_stock=5
    )

    fake_reorder_repo = MagicMock()

    use_case = CalculateReorderPointUseCase(
        product_repo=fake_product_repo,
        inventory_repo=fake_inventory_repo,
        reorder_repo=fake_reorder_repo,
        demand_std_dev=1.5,
    )

    forecast = ForecastResult(product_id="B1", predicted_demand=3.0, model_version="dummy-v0")
    result = use_case.execute(product_id="B1", forecast=forecast)

    assert result.needs_restock is True
    fake_reorder_repo.save.assert_called_once_with(result)


def test_does_not_need_restock_when_stock_is_high():
    fake_product_repo = MagicMock()
    fake_product_repo.get_by_id.return_value = Product(
        id="B1", sku="SKU-1", name="Baju Barong", lead_time_days=3
    )

    fake_inventory_repo = MagicMock()
    fake_inventory_repo.get_by_product_id.return_value = InventoryItem(
        product_id="B1", current_stock=500
    )

    fake_reorder_repo = MagicMock()

    use_case = CalculateReorderPointUseCase(
        product_repo=fake_product_repo,
        inventory_repo=fake_inventory_repo,
        reorder_repo=fake_reorder_repo,
        demand_std_dev=1.0,
    )

    forecast = ForecastResult(product_id="B1", predicted_demand=2.0, model_version="dummy-v0")
    result = use_case.execute(product_id="B1", forecast=forecast)

    assert result.needs_restock is False
    assert result.recommended_qty == 0
