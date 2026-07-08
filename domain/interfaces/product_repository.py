from abc import ABC, abstractmethod
from typing import List

from domain.entities.product import Product


class ProductRepository(ABC):

    @abstractmethod
    def get_by_id(self, product_id: str) -> Product:
        raise NotImplementedError

    @abstractmethod
    def list_active_products(self) -> List[Product]:
        raise NotImplementedError
