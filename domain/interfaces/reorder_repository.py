from abc import ABC, abstractmethod

from domain.entities.reorder_recommendation import ReorderRecommendation


class ReorderRepository(ABC):

    @abstractmethod
    def save(self, recommendation: ReorderRecommendation) -> None:
        raise NotImplementedError
