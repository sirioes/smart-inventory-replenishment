from dataclasses import dataclass


@dataclass
class ReorderRecommendation:
    product_id: str
    reorder_point: float
    recommended_qty: int
    needs_restock: bool
