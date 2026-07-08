from dataclasses import dataclass


@dataclass
class InventoryItem:
    product_id: str
    current_stock: int
    safety_stock: int = 0

    def __post_init__(self) -> None:
        if self.current_stock < 0:
            raise ValueError("current_stock tidak boleh negatif")
        if self.safety_stock < 0:
            raise ValueError("safety_stock tidak boleh negatif")
