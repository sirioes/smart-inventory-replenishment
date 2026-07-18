from sqlalchemy import create_engine, inspect

from infrastructure.db.models import Base


def _create_test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


def test_all_six_tables_created():
    engine = _create_test_engine()
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())

    expected_tables = {
        "products", "transactions", "inventory_items",
        "forecast_results", "reorder_recommendations", "alerts",
    }
    assert expected_tables.issubset(table_names)


def test_products_table_has_expected_columns():
    engine = _create_test_engine()
    inspector = inspect(engine)
    columns = {col["name"] for col in inspector.get_columns("products")}

    expected = {"id", "sku", "name", "unit_price", "lead_time_days", "created_at"}
    assert expected.issubset(columns)


def test_transactions_table_has_foreign_key_to_products():
    engine = _create_test_engine()
    inspector = inspect(engine)
    fks = inspector.get_foreign_keys("transactions")

    assert any(fk["referred_table"] == "products" for fk in fks)


def test_inventory_items_product_id_is_unique():
    engine = _create_test_engine()
    inspector = inspect(engine)
    unique_constraints = inspector.get_unique_constraints("inventory_items")

    has_unique_product_id = any(
        "product_id" in uc["column_names"] for uc in unique_constraints
    )
    assert has_unique_product_id


def test_alerts_table_has_foreign_key_to_reorder_recommendations():
    engine = _create_test_engine()
    inspector = inspect(engine)
    fks = inspector.get_foreign_keys("alerts")

    assert any(fk["referred_table"] == "reorder_recommendations" for fk in fks)
