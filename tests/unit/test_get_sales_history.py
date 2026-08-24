from unittest.mock import MagicMock

import pytest

from application.use_cases.get_sales_history import GetSalesHistoryUseCase
from domain.entities.product import Product


def test_get_sales_history_returns_transactions_for_product():
    product_repo = MagicMock()
    product_repo.get_by_id.return_value = Product(
        id="P1", sku="SKU-1", name="Widget", lead_time_days=3
    )

    transaction_repo = MagicMock()
    transaction_repo.get_history.return_value = [
        {"transaction_date": "2026-08-01", "quantity_sold": 5, "is_promo": 0},
        {"transaction_date": "2026-08-02", "quantity_sold": 8, "is_promo": 1},
    ]

    use_case = GetSalesHistoryUseCase(
        product_repo=product_repo, transaction_repo=transaction_repo
    )

    result = use_case.execute(product_id="P1")

    assert len(result) == 2
    assert result[0]["quantity_sold"] == 5
    product_repo.get_by_id.assert_called_once_with("P1")
    transaction_repo.get_history.assert_called_once_with("P1")


def test_get_sales_history_raises_when_product_missing():
    product_repo = MagicMock()
    product_repo.get_by_id.side_effect = ValueError(
        "Product dengan id=missing-id tidak ditemukan"
    )
    transaction_repo = MagicMock()

    use_case = GetSalesHistoryUseCase(
        product_repo=product_repo, transaction_repo=transaction_repo
    )

    with pytest.raises(ValueError):
        use_case.execute(product_id="missing-id")

    transaction_repo.get_history.assert_not_called()
