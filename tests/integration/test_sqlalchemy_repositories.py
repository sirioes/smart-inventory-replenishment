from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.entities.forecast_result import ForecastResult
from domain.entities.reorder_recommendation import ReorderRecommendation
from infrastructure.db.models import (
    Base,
    ForecastResultModel,
    InventoryItemModel,
    ProductModel,
    ReorderRecommendationModel,
    TransactionModel,
)
from infrastructure.repositories.sqlalchemy_forecast_repository import (
    SQLAlchemyForecastRepository,
)
from infrastructure.repositories.sqlalchemy_inventory_repository import (
    SQLAlchemyInventoryRepository,
)
from infrastructure.repositories.sqlalchemy_product_repository import (
    SQLAlchemyProductRepository,
)
from infrastructure.repositories.sqlalchemy_reorder_repository import (
    SQLAlchemyReorderRepository,
)
from infrastructure.repositories.sqlalchemy_transaction_repository import (
    SQLAlchemyTransactionRepository,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db_session = SessionLocal()
    yield db_session
    db_session.close()


def test_product_repository_get_by_id(session):
    session.add(ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7, unit_price=23000))
    session.commit()

    repo = SQLAlchemyProductRepository(session)
    product = repo.get_by_id("A3")

    assert product.id == "A3"
    assert product.sku == "SKU-5"
    assert product.lead_time_days == 7


def test_product_repository_raises_error_when_not_found(session):
    repo = SQLAlchemyProductRepository(session)
    with pytest.raises(ValueError):
        repo.get_by_id("tidak-ada")


def test_product_repository_list_active_products(session):
    session.add_all([
        ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7),
        ProductModel(id="M2", sku="SKU-3", name="Pisang Keju", lead_time_days=3),
    ])
    session.commit()

    repo = SQLAlchemyProductRepository(session)
    products = repo.list_active_products()

    assert len(products) == 2


def test_transaction_repository_get_history_ordered_by_date(session):
    session.add(ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7))
    session.add_all([
        TransactionModel(product_id="A3", quantity_sold=10, transaction_date=date(2024, 1, 2), is_promo=False),
        TransactionModel(product_id="A3", quantity_sold=5, transaction_date=date(2024, 1, 1), is_promo=True),
    ])
    session.commit()

    repo = SQLAlchemyTransactionRepository(session)
    history = repo.get_history("A3")

    assert len(history) == 2
    assert history[0]["transaction_date"] == "2024-01-01"
    assert history[0]["quantity_sold"] == 5
    assert history[0]["is_promo"] == 1


def test_inventory_repository_get_by_product_id(session):
    session.add(ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7))
    session.add(InventoryItemModel(product_id="A3", current_stock=50, safety_stock=10))
    session.commit()

    repo = SQLAlchemyInventoryRepository(session)
    item = repo.get_by_product_id("A3")

    assert item.current_stock == 50
    assert item.safety_stock == 10


def test_forecast_repository_save_persists_row(session):
    session.add(ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7))
    session.commit()

    repo = SQLAlchemyForecastRepository(session)
    forecast = ForecastResult(product_id="A3", predicted_demand=42.5, model_version="xgboost-v1")
    repo.save(forecast)

    saved = session.query(ForecastResultModel).filter_by(product_id="A3").first()
    assert saved is not None
    assert saved.predicted_demand == 42.5
    assert saved.model_version == "xgboost-v1"


def test_reorder_repository_save_persists_row(session):
    session.add(ProductModel(id="A3", sku="SKU-5", name="Gelang Kerang", lead_time_days=7))
    session.commit()

    repo = SQLAlchemyReorderRepository(session)
    recommendation = ReorderRecommendation(
        product_id="A3", reorder_point=30.0, recommended_qty=10, needs_restock=True
    )
    repo.save(recommendation)

    saved = session.query(ReorderRecommendationModel).filter_by(product_id="A3").first()
    assert saved is not None
    assert saved.needs_restock is True
    assert saved.recommended_qty == 10
