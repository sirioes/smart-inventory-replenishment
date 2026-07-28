from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class ForecastResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: str = Field(..., description="Unique identifier of the product.")
    predicted_demand: float = Field(
        ..., ge=0, description="Predicted demand quantity for the target date."
    )
    model_version: str = Field(
        ..., description="Version identifier of the forecasting model used."
    )
    forecast_date: Optional[date] = Field(
        None, description="Target date of the prediction."
    )
