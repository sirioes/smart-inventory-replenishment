from abc import ABC, abstractmethod
from typing import List

from domain.entities.inventory_item import InventoryItem


class InventoryRepository(ABC):

    @abstractmethod
    def get_by_product_id(self, product_id: str) -> InventoryItem:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[InventoryItem]:
        raise NotImplementedError
