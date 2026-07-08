from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ForecastResult:
    product_id: str
    predicted_demand: float
    model_version: str
    forecast_date: Optional[date] = None

    def __post_init__(self) -> None:
        if self.predicted_demand < 0:
            raise ValueError("predicted_demand tidak boleh negatif")
