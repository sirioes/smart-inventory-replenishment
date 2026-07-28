from datetime import datetime, timezone
from fastapi import FastAPI
from api.routes import forecasts, inventory
from api.schemas.health_schema import HealthResponse

app = FastAPI(
    title="Smart Inventory Replenishment System",
    description="Demand forecasting and automated restock recommendation API.",
    version="0.3.0",
)

app.include_router(inventory.router)
app.include_router(forecasts.router)

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="Report service liveness",
)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))
