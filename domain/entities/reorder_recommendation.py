from dataclasses import dataclass
from typing import Optional


@dataclass
class ReorderRecommendation:
    product_id: str
    reorder_point: float
    recommended_qty: int
    needs_restock: bool
    id: Optional[str] = None
