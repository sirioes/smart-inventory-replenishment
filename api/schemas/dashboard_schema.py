from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductDashboardItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: str = Field(..., description="Unique identifier of the product.")
    sku: str = Field(..., description="Stock keeping unit code.")
    name: str = Field(..., description="Product display name.")
    current_stock: int = Field(..., ge=0, description="Current stock on hand.")
    safety_stock: int = Field(..., ge=0, description="Configured safety stock buffer.")
    reorder_point: Optional[float] = Field(
        None, description="Latest calculated reorder point, if one has been run."
    )
    recommended_qty: Optional[int] = Field(
        None, description="Latest recommended restock quantity, if one has been run."
    )
    needs_restock: bool = Field(
        ..., description="Whether the latest recommendation flags this product for restock."
    )
    open_alert_count: int = Field(
        ..., ge=0, description="Number of open alerts linked to this product."
    )


class DashboardResponse(BaseModel):
    products: list[ProductDashboardItem] = Field(
        ..., description="One row per active product."
    )
    generated_at: datetime = Field(
        ..., description="Server time at which this snapshot was assembled."
    )
