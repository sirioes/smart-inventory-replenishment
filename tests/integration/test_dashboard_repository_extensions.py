from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.db.models import (
    AlertModel,
    Base,
    ForecastResultModel,
    InventoryItemModel,
    ProductModel,
    ReorderRecommendationModel,
)
from infrastructure.repositories.sqlalchemy_alert_repository import (
    SQLAlchemyAlertRepository,
)
from infrastructure.repositories.sqlalchemy_forecast_repository import (
    SQLAlchemyForecastRepository,
)
from infrastructure.repositories.sqlalchemy_inventory_repository import (
    SQLAlchemyInventoryRepository,
)
from infrastructure.repositories.sqlalchemy_reorder_repository import (
    SQLAlchemyReorderRepository,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db_session = SessionLocal()
    yield db_session
    db_session.close()


def test_inventory_repository_list_all_returns_every_row(session):
    session.add_all([
        ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7),
        ProductModel(id="M2", sku="SKU-3", name="Pisang Keju", lead_time_days=3),
    ])
    session.add_all([
        InventoryItemModel(product_id="A3", current_stock=50, safety_stock=10),
        InventoryItemModel(product_id="M2", current_stock=8, safety_stock=15),
    ])
    session.commit()

    repo = SQLAlchemyInventoryRepository(session)
    items = repo.list_all()

    assert {item.product_id for item in items} == {"A3", "M2"}


def test_reorder_repository_get_latest_by_product_id_returns_most_recent(session):
    session.add(ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7))
    session.commit()

    repo = SQLAlchemyReorderRepository(session)
    older = ReorderRecommendationModel(
        product_id="A3", reorder_point=10.0, recommended_qty=5, needs_restock=False
    )
    session.add(older)
    session.commit()

    newer = ReorderRecommendationModel(
        product_id="A3", reorder_point=30.0, recommended_qty=20, needs_restock=True
    )
    session.add(newer)
    session.commit()

    latest = repo.get_latest_by_product_id("A3")

    assert latest is not None
    assert latest.recommended_qty == 20
    assert latest.needs_restock is True


def test_reorder_repository_get_latest_by_product_id_returns_none_when_absent(session):
    session.add(ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7))
    session.commit()

    repo = SQLAlchemyReorderRepository(session)

    assert repo.get_latest_by_product_id("A3") is None


def test_forecast_repository_list_by_product_id_orders_oldest_first(session):
    session.add(ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7))
    session.add_all([
        ForecastResultModel(
            product_id="A3", predicted_demand=12.0, model_version="xgboost-v1",
            forecast_date=date(2026, 8, 8),
        ),
        ForecastResultModel(
            product_id="A3", predicted_demand=10.0, model_version="xgboost-v1",
            forecast_date=date(2026, 8, 1),
        ),
    ])
    session.commit()

    repo = SQLAlchemyForecastRepository(session)
    history = repo.list_by_product_id("A3")

    assert [h.forecast_date for h in history] == [date(2026, 8, 1), date(2026, 8, 8)]


def test_alert_repository_count_open_for_product_joins_through_recommendation(session):
    session.add_all([
        ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7),
        ProductModel(id="M2", sku="SKU-3", name="Pisang Keju", lead_time_days=3),
    ])
    session.commit()

    rec_a3 = ReorderRecommendationModel(
        product_id="A3", reorder_point=10.0, recommended_qty=5, needs_restock=True
    )
    rec_m2 = ReorderRecommendationModel(
        product_id="M2", reorder_point=8.0, recommended_qty=3, needs_restock=True
    )
    session.add_all([rec_a3, rec_m2])
    session.commit()

    session.add_all([
        AlertModel(recommendation_id=rec_a3.id, status="open", channel="dashboard"),
        AlertModel(recommendation_id=rec_a3.id, status="open", channel="email"),
        AlertModel(recommendation_id=rec_a3.id, status="resolved", channel="dashboard"),
        # Different product entirely — must not leak into A3's count.
        AlertModel(recommendation_id=rec_m2.id, status="open", channel="dashboard"),
    ])
    session.commit()

    repo = SQLAlchemyAlertRepository(session)

    assert repo.count_open_for_product("A3") == 2
    assert repo.count_open_for_product("M2") == 1
