from unittest.mock import MagicMock

from application.use_cases.get_dashboard_data import GetDashboardDataUseCase
from domain.entities.inventory_item import InventoryItem
from domain.entities.product import Product
from domain.entities.reorder_recommendation import ReorderRecommendation


def _make_use_case(**overrides):
    # Arrange: siapkan mock untuk semua repository, tanpa database sungguhan
    defaults = dict(
        product_repo=MagicMock(),
        inventory_repo=MagicMock(),
        reorder_repo=MagicMock(),
        alert_repo=MagicMock(),
    )
    defaults.update(overrides)
    return GetDashboardDataUseCase(**defaults), defaults


def test_dashboard_aggregates_product_inventory_reorder_and_alerts():
    product_repo = MagicMock()
    product_repo.list_active_products.return_value = [
        Product(id="P1", sku="SKU-1", name="Widget", lead_time_days=3),
    ]

    inventory_repo = MagicMock()
    inventory_repo.list_all.return_value = [
        InventoryItem(product_id="P1", current_stock=5, safety_stock=10),
    ]

    reorder_repo = MagicMock()
    reorder_repo.get_latest_by_product_id.return_value = ReorderRecommendation(
        product_id="P1", reorder_point=12.0, recommended_qty=20, needs_restock=True
    )

    alert_repo = MagicMock()
    alert_repo.count_open_for_product.return_value = 2

    use_case, _ = _make_use_case(
        product_repo=product_repo,
        inventory_repo=inventory_repo,
        reorder_repo=reorder_repo,
        alert_repo=alert_repo,
    )

    # Act
    result = use_case.execute()

    # Assert
    assert len(result) == 1
    row = result[0]
    assert row.product_id == "P1"
    assert row.sku == "SKU-1"
    assert row.current_stock == 5
    assert row.safety_stock == 10
    assert row.needs_restock is True
    assert row.recommended_qty == 20
    assert row.open_alert_count == 2
    alert_repo.count_open_for_product.assert_called_once_with("P1")


def test_dashboard_handles_product_with_no_inventory_or_recommendation_yet():
    product_repo = MagicMock()
    product_repo.list_active_products.return_value = [
        Product(id="P2", sku="SKU-2", name="Gadget", lead_time_days=5),
    ]

    inventory_repo = MagicMock()
    inventory_repo.list_all.return_value = []  # belum ada InventoryItem utk produk ini

    reorder_repo = MagicMock()
    reorder_repo.get_latest_by_product_id.return_value = None  # belum pernah diproses

    alert_repo = MagicMock()
    alert_repo.count_open_for_product.return_value = 0

    use_case, _ = _make_use_case(
        product_repo=product_repo,
        inventory_repo=inventory_repo,
        reorder_repo=reorder_repo,
        alert_repo=alert_repo,
    )

    result = use_case.execute()

    row = result[0]
    assert row.current_stock == 0
    assert row.safety_stock == 0
    assert row.reorder_point is None
    assert row.recommended_qty is None
    assert row.needs_restock is False
