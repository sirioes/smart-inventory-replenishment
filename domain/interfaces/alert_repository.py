from abc import ABC, abstractmethod

from domain.entities.alert import Alert

class AlertRepository(ABC):

    @abstractmethod
    def save(self, alert: Alert) -> None:
        raise NotImplementedError

    @abstractmethod
    def count_open_for_product(self, product_id: str) -> int:
        """Count open alerts for a product.

        Alert only carries `recommendation_id` (not `product_id`), so
        resolving "open alerts for this product" requires joining through
        ReorderRecommendation. That join is an infrastructure concern —
        this method keeps it out of the application layer.
        """
        raise NotImplementedError
