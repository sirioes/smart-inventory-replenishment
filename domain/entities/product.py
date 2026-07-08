from dataclasses import dataclass


@dataclass
class Product:

    id: str
    sku: str
    name: str
    lead_time_days: int
    unit_price: float = 0.0

    def __post_init__(self) -> None:
        if self.lead_time_days < 0:
            raise ValueError("lead_time_days tidak boleh negatif")
        if self.unit_price < 0:
            raise ValueError("unit_price tidak boleh negatif")
