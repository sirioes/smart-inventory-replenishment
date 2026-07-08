from abc import ABC, abstractmethod

from domain.entities.inventory_item import InventoryItem


class InventoryRepository(ABC):

    @abstractmethod
    def get_by_product_id(self, product_id: str) -> InventoryItem:
        raise NotImplementedError
