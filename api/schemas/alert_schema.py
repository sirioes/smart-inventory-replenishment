from pydantic import BaseModel


class AlertFeedItem(BaseModel):
    alert_id: str
    product_id: str
    sku: str
    name: str
    status: str
    channel: str
    created_at: str
    recommended_qty: int
