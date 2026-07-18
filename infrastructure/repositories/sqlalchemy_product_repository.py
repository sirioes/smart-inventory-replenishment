from typing import List

from sqlalchemy.orm import Session

from domain.entities.product import Product
from domain.interfaces.product_repository import ProductRepository
from infrastructure.db.models import ProductModel


class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, product_id: str) -> Product:
        row = self.session.get(ProductModel, product_id)
        if row is None:
            raise ValueError(f"Product dengan id={product_id} tidak ditemukan")
        return self._to_entity(row)

    def list_active_products(self) -> List[Product]:
        rows = self.session.query(ProductModel).all()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row: ProductModel) -> Product:
        return Product(
            id=row.id,
            sku=row.sku,
            name=row.name,
            lead_time_days=row.lead_time_days,
            unit_price=row.unit_price,
        )
