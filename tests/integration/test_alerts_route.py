from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_alerts_feed_use_case
from api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture(autouse=True)
def _clear_overrides():
    yield
    app.dependency_overrides.clear()

def test_list_alerts_returns_items(client: TestClient) -> None:
    fake_use_case = MagicMock()
    fake_use_case.execute.return_value = [
        {
            "alert_id": "A1",
            "product_id": "P1",
            "sku": "SKU-1",
            "name": "Widget",
            "status": "open",
            "channel": "log",
            "created_at": "2026-08-01T10:00:00",
            "recommended_qty": 20,
        }
    ]
    app.dependency_overrides[get_alerts_feed_use_case] = lambda: fake_use_case

    response = client.get("/alerts")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["status"] == "open"

def test_list_alerts_returns_empty_list_when_none(client: TestClient) -> None:
    fake_use_case = MagicMock()
    fake_use_case.execute.return_value = []
    app.dependency_overrides[get_alerts_feed_use_case] = lambda: fake_use_case

    response = client.get("/alerts")

    assert response.status_code == 200
    assert response.json() == []
