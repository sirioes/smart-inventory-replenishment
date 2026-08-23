from typing import List

from sqlalchemy.orm import Session

from domain.entities.inventory_item import InventoryItem
from domain.interfaces.inventory_repository import InventoryRepository
from infrastructure.db.models import InventoryItemModel


class SQLAlchemyInventoryRepository(InventoryRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_product_id(self, product_id: str) -> InventoryItem:
        row = (
            self.session.query(InventoryItemModel)
            .filter(InventoryItemModel.product_id == product_id)
            .first()
        )
        if row is None:
            raise ValueError(f"InventoryItem untuk product_id={product_id} tidak ditemukan")
        return self._to_entity(row)

    def list_all(self) -> List[InventoryItem]:
        rows = self.session.query(InventoryItemModel).all()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row: InventoryItemModel) -> InventoryItem:
        return InventoryItem(
            product_id=row.product_id,
            current_stock=row.current_stock,
            safety_stock=row.safety_stock,
        )
