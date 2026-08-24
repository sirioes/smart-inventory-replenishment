import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import dashboard, forecasts, inventory, sales
from api.schemas.health_schema import HealthResponse

app = FastAPI(
    title="Smart Inventory Replenishment System",
    description="Demand forecasting and automated restock recommendation API.",
    version="0.4.0",
)

# Comma-separated list, e.g. "http://localhost:3000,https://myapp.vercel.app".
# Defaults to the Next.js dev server so `npm run dev` works against a local
# API with zero extra setup.
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory.router)
app.include_router(forecasts.router)
app.include_router(dashboard.router)
app.include_router(sales.router)

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="Report service liveness",
)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))
