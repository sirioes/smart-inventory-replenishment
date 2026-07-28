from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from api.dependencies import get_facade
from api.main import app
from domain.entities.reorder_recommendation import ReorderRecommendation


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture(autouse=True)
def _clear_overrides():
    yield
    app.dependency_overrides.clear()

def test_process_product_returns_recommendation(client: TestClient) -> None:
    fake_facade = MagicMock()
    fake_facade.process_product.return_value = ReorderRecommendation(
        product_id="B1",
        reorder_point=42.0,
        recommended_qty=100,
        needs_restock=True,
    )
    app.dependency_overrides[get_facade] = lambda: fake_facade

    response = client.post("/products/B1/process")

    assert response.status_code == 200
    body = response.json()
    assert body["product_id"] == "B1"
    assert body["needs_restock"] is True
    assert body["recommended_qty"] == 100
    fake_facade.process_product.assert_called_once_with(product_id="B1")

def test_process_product_returns_404_when_product_missing(client: TestClient) -> None:
    fake_facade = MagicMock()
    fake_facade.process_product.side_effect = ValueError(
        "Product dengan id=missing-id tidak ditemukan"
    )
    app.dependency_overrides[get_facade] = lambda: fake_facade

    response = client.post("/products/missing-id/process")

    assert response.status_code == 404
    assert "missing-id" in response.json()["detail"]
