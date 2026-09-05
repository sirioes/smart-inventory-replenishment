# Smart Inventory Replenishment System

Demand forecasting and automated restock recommendation system for retail, built with Clean Architecture and GoF Design Patterns.

`Python 3.13` `FastAPI` `XGBoost` `PostgreSQL 16` `Groq` `Next.js` `Docker`

**Status:** Sprint 4 — User Interface, GenAI Chat Assistant & Deployment (Complete)

## Overview

Retailers routinely face the same trade-off: too much stock ties up capital in storage, too little causes stockouts and lost sales. This system automates the "when and how much to restock" decision by combining ML-based demand forecasting (XGBoost) with classic supply-chain formulas (reorder point, safety stock), and exposes the results through a dashboard and a natural-language chat assistant.

The project also doubles as a demonstration of production-grade engineering practices: a 4-layer Clean Architecture backend, four GoF design patterns applied to real problems (not bolted on for show), a token-driven themeable frontend, and a fully containerized deployment.

## Key Features

- **Demand forecasting** per SKU using XGBoost, with engineered lag/rolling-window features and cyclical calendar encoding
- **Reorder point & safety stock calculation** driven by XGBoost forecasts, benchmarked against a naive baseline
- **Event-driven alerts** (Observer pattern) dispatched to dashboard, email, and log channels when stock falls below its reorder point
- **Dashboard** (Next.js + Recharts) — inventory status, forecast vs. actual charts, restock recommendations, light/dark theme
- **Natural-language chat assistant** (Groq API) for querying inventory state in plain language — e.g. *"produk apa yang perlu direstock minggu ini?"*
- **One-command local deployment** via Docker Compose (frontend, API, and database)

## Architecture

The backend follows Clean Architecture's dependency rule: dependencies only point inward, and the domain layer has zero knowledge of FastAPI, SQLAlchemy, XGBoost, or the Groq SDK.

```
Frameworks & Drivers   →  api/            FastAPI routes, thin controllers
Interface Adapters     →  infrastructure/ concrete implementations
Use Cases              →  application/    business logic, orchestration
Entities               →  domain/         pure business rules, no external deps
```

### Design Patterns

| Pattern | Layer | Problem it solves |
|---|---|---|
| **Strategy** | `domain/interfaces/forecast_strategy.py` + `infrastructure/ml/xgboost_strategy.py` | Forecasting model can be swapped without touching use cases |
| **Repository** | `domain/interfaces/*_repository.py` (product, transaction, forecast, inventory, reorder, alert) + `infrastructure/repositories/` | Use cases depend on an interface, not SQLAlchemy directly — testable without a live database |
| **Observer** | `domain/interfaces/notifier.py` + `infrastructure/notifiers/` (dashboard, email, log) | One event (stock below reorder point) fans out to three channels without coupling them together |
| **Facade** | `application/inventory_service_facade.py` | Orchestrates forecast → reorder point → alert as one call, keeping the API controller thin |
| **Adapter** | `domain/interfaces/llm_provider.py` + `infrastructure/llm/groq_adapter.py` | Isolates the Groq SDK behind a provider-agnostic interface — no other module imports `groq` directly |

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13, FastAPI 0.115.5 |
| ML | XGBoost 2.1.2, pandas 2.2.3, scikit-learn 1.5.2, numpy 2.1.3 |
| Database | PostgreSQL 16 (Alpine), SQLAlchemy 2.0.36 |
| LLM | Groq API — `openai/gpt-oss-20b` by default (configurable via `GROQ_MODEL`), chosen over Llama models per Groq's current model recommendations |
| Frontend | Next.js (App Router), TypeScript, Tailwind CSS, Recharts, lucide-react |
| Testing | pytest 8.3.3 (backend), ESLint + `tsc --noEmit` (frontend) |
| Containerization | Docker, Docker Compose |

## Project Structure

```
smart-inventory-replenishment/
├── domain/                  # Entities & interfaces — no framework dependencies
│   ├── entities/
│   └── interfaces/
├── application/             # Use cases + inventory_service_facade.py
│   └── use_cases/
├── infrastructure/          # Concrete implementations
│   ├── db/                  # SQLAlchemy models & session config
│   ├── llm/                 # groq_adapter.py
│   ├── ml/                  # xgboost_strategy.py, feature_engineering.py, model_evaluation.py, model_registry/
│   ├── notifiers/           # dashboard_notifier.py, email_notifier.py, log_notifier.py
│   └── repositories/        # Concrete repository implementations
├── api/                     # FastAPI routes (thin controllers)
├── scripts/                 # DB setup, seeding, training scripts
├── data/raw/                # Training datasets
├── tests/                   # Unit tests + integration tests
├── frontend/                # Next.js dashboard
│   ├── app/                 # Routes: overview, inventory, forecasts, alerts, assistant
│   ├── components/          # Sidebar, Topbar, ThemeToggle, shared UI
│   ├── lib/                 # Typed API client
│   ├── types/
│   └── Dockerfile           # Frontend image
├── docker-compose.yml
├── Dockerfile               # API image
├── requirements.txt
└── .env.example
```

## Getting Started

### Prerequisites

- Docker & Docker Compose (recommended path), **or** Python 3.13 and Node.js 20+ for running services individually
- A [Groq API key](https://console.groq.com) for the chat assistant

### Environment Variables

Copy the example file and fill in real values:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Database credentials |
| `DATABASE_URL` | Assembled automatically inside Docker Compose from the credentials above |
| `GROQ_API_KEY` | Required for the chat assistant to return real responses |

### Run with Docker Compose (recommended)

```bash
docker compose up --build
```

This builds and starts the frontend, API, and PostgreSQL database together, with the database gated behind a health check so the API doesn't start until it's ready to accept connections.

| Service | URL |
|---|---|
| Frontend dashboard | http://localhost:3000 |
| API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |

To stop the stack while keeping data: `docker compose down`
To stop and wipe the database volume: `docker compose down -v`

### Run Locally (without Docker)

**Backend:**
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Testing

```bash
# Backend
python -m pytest -v

# Frontend
cd frontend
npm run lint
npm run typecheck
```

## ML Model Evaluation

| Metric | XGBoost | Baseline (naive) |
|---|---|---|
| MAE | 87.384 | 118.531 |
| MAPE | 292.4% | 319.5% |
| WAPE | 64.8% | 88.0% |
| **Improvement over baseline** | **26.28%** | — |

**Reading these numbers:** MAPE looks high for both models because of intermittent near-zero daily demand — WAPE is the more reliable metric here, and it shows XGBoost meaningfully outperforming the baseline.

> **In progress:** Updated metrics will replace this table once retraining on the corrected dataset is complete.

## Development Workflow

- **Branching:** `feat/issue-[id]-short-description`
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/)
- **Tracking:** GitHub Projects board, one issue per feature, PRs linked with `Closes #XX`

## Known Limitations

- **No authentication.** The dashboard's user avatar and Logout control are static UI placeholders — there's no login system or session management wired up yet.
- **No automated scheduling.** Forecasting and reorder-point recalculation currently only run when triggered manually via POST /products/{id}/process — nothing re-runs this automatically on a schedule.
- CI/CD (GitHub Actions) is not configured — there's no .github/workflows/ directory in the repo, so tests are run manually rather than on every push. 
- Reorder point evaluation requires seeded transaction history per product — some demo-seeded products have inventory data but not transaction history, so /products/{id}/process will 404 for those until seeding is extended
- Model evaluation numbers above will be superseded once the training dataset migration is complete

## License

Built as a portfolio project for internship applications.