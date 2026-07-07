# Smart Inventory Replenishment System

Sistem prediksi demand dan rekomendasi restock otomatis untuk retail,
dibangun dengan Clean Architecture dan GoF Design Pattern.

**Status:** Sprint 1 - Domain Layer, Core Interfaces & Use Cases

## Cara menjalankan test

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -v
```

## Struktur project

- `domain/` - entities & interfaces (business rules murni, tanpa dependency eksternal)
- `application/` - use cases (logika aplikasi, dependency injection)
- `infrastructure/` - implementasi konkret (database, ML) - mulai Sprint 2
- `api/` - FastAPI routes - mulai Sprint 3
- `tests/` - unit test dengan mock repository