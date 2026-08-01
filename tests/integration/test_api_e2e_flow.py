from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.main import app
from infrastructure.db.models import (
    AlertModel,
    Base,
    InventoryItemModel,
    ProductModel,
    TransactionModel,
)
from infrastructure.db.session import get_session

def _seed_product(
    session, product_id: str, current_stock: int, lead_time_days: int = 7
) -> None:
    session.add(
        ProductModel(
            id=product_id,
            sku=f"SKU-{product_id}",
            name="E2E Test Product",
            lead_time_days=lead_time_days,
        )
    )
    session.add(
        InventoryItemModel(
            product_id=product_id, current_stock=current_stock, safety_stock=0
        )
    )
    start = date(2026, 6, 1)
    for i in range(45):
        session.add(
            TransactionModel(
                product_id=product_id,
                quantity_sold=10 + (i % 5),
                transaction_date=start + timedelta(days=i),
                is_promo=False,
            )
        )
    session.commit()

@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(bind=test_engine)
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
def client(test_engine):
    TestingSessionLocal = sessionmaker(bind=test_engine)

    def override_get_session():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_forecast_endpoint_returns_real_forecast_for_seeded_product(client, db_session):
    _seed_product(db_session, "E2E-FORECAST", current_stock=100)

    response = client.post("/products/E2E-FORECAST/forecast")

    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "product_id",
        "predicted_demand",
        "model_version",
        "forecast_date",
    }
    assert body["product_id"] == "E2E-FORECAST"
    assert body["predicted_demand"] >= 0
    assert body["model_version"] == "xgboost-v1"

def test_forecast_endpoint_returns_404_for_unknown_product(client):
    response = client.post("/products/does-not-exist/forecast")

    assert response.status_code == 404

def test_process_endpoint_triggers_alert_when_stock_is_low(client, db_session):
    _seed_product(db_session, "E2E-LOW-STOCK", current_stock=1)

    response = client.post("/products/E2E-LOW-STOCK/process")

    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "product_id",
        "reorder_point",
        "recommended_qty",
        "needs_restock",
    }
    assert body["needs_restock"] is True

    alerts = db_session.query(AlertModel).all()
    assert len(alerts) == 1
    assert alerts[0].channel == "dashboard"
    assert alerts[0].status == "open"

def test_process_endpoint_does_not_trigger_alert_when_stock_is_healthy(
    client, db_session
):
    _seed_product(db_session, "E2E-HIGH-STOCK", current_stock=1_000_000)

    response = client.post("/products/E2E-HIGH-STOCK/process")

    assert response.status_code == 200
    assert response.json()["needs_restock"] is False
    assert db_session.query(AlertModel).count() == 0

def test_process_endpoint_returns_404_for_unknown_product(client):
    response = client.post("/products/does-not-exist/process")

    assert response.status_code == 404
