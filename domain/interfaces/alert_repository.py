from abc import ABC, abstractmethod
from typing import Any, Dict, List

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

    @abstractmethod
    def list_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List recent alerts joined with their product context."""
        raise NotImplementedError
