from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_dashboard_use_case
from api.main import app
from application.use_cases.get_dashboard_data import ProductDashboardData


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture(autouse=True)
def _clear_overrides():
    yield
    app.dependency_overrides.clear()

def test_get_dashboard_returns_aggregated_rows(client: TestClient) -> None:
    fake_use_case = MagicMock()
    fake_use_case.execute.return_value = [
        ProductDashboardData(
            product_id="P1",
            sku="SKU-1",
            name="Widget",
            current_stock=5,
            safety_stock=10,
            reorder_point=12.0,
            recommended_qty=20,
            needs_restock=True,
            open_alert_count=2,
        )
    ]
    app.dependency_overrides[get_dashboard_use_case] = lambda: fake_use_case

    response = client.get("/dashboard")

    assert response.status_code == 200
    body = response.json()
    assert len(body["products"]) == 1
    assert body["products"][0]["product_id"] == "P1"
    assert body["products"][0]["needs_restock"] is True
    assert "generated_at" in body

def test_get_dashboard_returns_empty_list_when_no_products(client: TestClient) -> None:
    fake_use_case = MagicMock()
    fake_use_case.execute.return_value = []
    app.dependency_overrides[get_dashboard_use_case] = lambda: fake_use_case

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert response.json()["products"] == []
