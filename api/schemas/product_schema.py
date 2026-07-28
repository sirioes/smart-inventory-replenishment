from pydantic import BaseModel, ConfigDict, Field

class ReorderRecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: str = Field(..., description="Unique identifier of the product.")
    reorder_point: float = Field(
        ..., ge=0, description="Calculated stock level that triggers a reorder."
    )
    recommended_qty: int = Field(
        ..., ge=0, description="Recommended quantity to restock."
    )
    needs_restock: bool = Field(
        ..., description="Whether the product currently needs restocking."
    )
