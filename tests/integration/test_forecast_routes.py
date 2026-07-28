from datetime import date
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from api.dependencies import get_forecast_use_case
from api.main import app
from domain.entities.forecast_result import ForecastResult


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture(autouse=True)
def _clear_overrides():
    yield
    app.dependency_overrides.clear()

def test_trigger_forecast_returns_forecast(client: TestClient) -> None:
    fake_use_case = MagicMock()
    fake_use_case.execute.return_value = ForecastResult(
        product_id="M1",
        predicted_demand=12.5,
        model_version="xgboost-v1",
        forecast_date=date(2026, 7, 29),
    )
    app.dependency_overrides[get_forecast_use_case] = lambda: fake_use_case

    response = client.post("/products/M1/forecast")

    assert response.status_code == 200
    body = response.json()
    assert body["product_id"] == "M1"
    assert body["model_version"] == "xgboost-v1"
    assert body["predicted_demand"] == 12.5
    fake_use_case.execute.assert_called_once_with(product_id="M1")

def test_trigger_forecast_returns_404_when_product_missing(client: TestClient) -> None:
    fake_use_case = MagicMock()
    fake_use_case.execute.side_effect = ValueError(
        "Product dengan id=missing-id tidak ditemukan"
    )
    app.dependency_overrides[get_forecast_use_case] = lambda: fake_use_case

    response = client.post("/products/missing-id/forecast")

    assert response.status_code == 404
    assert "missing-id" in response.json()["detail"]
