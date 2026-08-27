import os
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.routes import alerts, chat, dashboard, forecasts, inventory, sales
from api.schemas.health_schema import HealthResponse
from domain.interfaces.llm_provider import LLMProviderError

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
app.include_router(alerts.router)
app.include_router(chat.router)

@app.exception_handler(LLMProviderError)
def handle_llm_provider_error(request: Request, exc: LLMProviderError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": f"Chat assistant sedang tidak bisa diakses: {exc}"},
    )

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="Report service liveness",
)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))
