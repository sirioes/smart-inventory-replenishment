from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_sales_history_use_case
from api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture(autouse=True)
def _clear_overrides():
    yield
    app.dependency_overrides.clear()

def test_list_sales_history_returns_transactions(client: TestClient) -> None:
    fake_use_case = MagicMock()
    fake_use_case.execute.return_value = [
        {"transaction_date": "2026-08-01", "quantity_sold": 5, "is_promo": False},
        {"transaction_date": "2026-08-02", "quantity_sold": 8, "is_promo": True},
    ]
    app.dependency_overrides[get_sales_history_use_case] = lambda: fake_use_case

    response = client.get("/products/P1/sales-history")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["quantity_sold"] == 5
    assert body[1]["is_promo"] is True
    fake_use_case.execute.assert_called_once_with(product_id="P1")

def test_list_sales_history_returns_404_when_product_missing(client: TestClient) -> None:
    fake_use_case = MagicMock()
    fake_use_case.execute.side_effect = ValueError(
        "Product dengan id=missing-id tidak ditemukan"
    )
    app.dependency_overrides[get_sales_history_use_case] = lambda: fake_use_case

    response = client.get("/products/missing-id/sales-history")

    assert response.status_code == 404
    assert "missing-id" in response.json()["detail"]
