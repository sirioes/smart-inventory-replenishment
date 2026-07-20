# Smart Inventory Replenishment System

Demand forecasting and automated restock recommendation system for retail, built with Clean Architecture and GoF Design Patterns.

**Status:** Sprint 3 - RESTful API Layer & Event-Driven Alerts

## How to Run Tests

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -v
```

## How to Run the API

```bash
uvicorn api.main:app --reload
```

## Project Structure

- `domain/` - entities & interfaces (pure business rules, no external dependency)
- `application/` - use cases (application logic, dependency injection) + `InventoryServiceFacade` (Sprint 3)
- `infrastructure/` - concrete implementations (database, ML - Sprint 2; notifiers for Observer pattern - Sprint 3)
- `api/` - FastAPI routes (Sprint 3)
- `tests/` - unit tests with mock repository + integration tests (Sprint 3)