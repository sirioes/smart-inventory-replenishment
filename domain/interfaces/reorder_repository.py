from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.reorder_recommendation import ReorderRecommendation


class ReorderRepository(ABC):

    @abstractmethod
    def save(self, recommendation: ReorderRecommendation) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_latest_by_product_id(self, product_id: str) -> Optional[ReorderRecommendation]:
        raise NotImplementedError
