from typing import Any, Dict, List

from sqlalchemy.orm import Session

from domain.interfaces.transaction_repository import TransactionRepository
from infrastructure.db.models import TransactionModel


class SQLAlchemyTransactionRepository(TransactionRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_history(self, product_id: str) -> List[Dict[str, Any]]:
        rows = (
            self.session.query(TransactionModel)
            .filter(TransactionModel.product_id == product_id)
            .order_by(TransactionModel.transaction_date)
            .all()
        )
        return [
            {
                "transaction_date": row.transaction_date.isoformat(),
                "quantity_sold": row.quantity_sold,
                "is_promo": int(row.is_promo),
            }
            for row in rows
        ]
