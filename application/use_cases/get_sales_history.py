from typing import Any, Dict, List

from domain.interfaces.product_repository import ProductRepository
from domain.interfaces.transaction_repository import TransactionRepository


class GetSalesHistoryUseCase:
    def __init__(
        self,
        product_repo: ProductRepository,
        transaction_repo: TransactionRepository,
    ) -> None:
        self.product_repo = product_repo
        self.transaction_repo = transaction_repo

    def execute(self, product_id: str) -> List[Dict[str, Any]]:
        self.product_repo.get_by_id(product_id)
        return self.transaction_repo.get_history(product_id)
