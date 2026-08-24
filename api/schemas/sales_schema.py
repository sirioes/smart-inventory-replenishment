from pydantic import BaseModel


class SalesHistoryItem(BaseModel):
    transaction_date: str
    quantity_sold: int
    is_promo: bool
