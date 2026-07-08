from abc import ABC, abstractmethod
from typing import Any, Dict, List


class TransactionRepository(ABC):

    @abstractmethod
    def get_history(self, product_id: str) -> List[Dict[str, Any]]:
        raise NotImplementedError
