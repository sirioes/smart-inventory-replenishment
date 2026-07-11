import pytest

from domain.entities.inventory_item import InventoryItem
from domain.entities.product import Product


def test_inventory_item_rejects_negative_stock():
    with pytest.raises(ValueError):
        InventoryItem(product_id="B1", current_stock=-5)


def test_product_rejects_negative_lead_time():
    with pytest.raises(ValueError):
        Product(id="B1", sku="SKU-1", name="Baju Barong", lead_time_days=-3)


def test_product_created_with_valid_data():
    product = Product(id="B1", sku="SKU-1", name="Baju Barong", lead_time_days=7)
    assert product.lead_time_days == 7
    assert product.unit_price == 0.0
