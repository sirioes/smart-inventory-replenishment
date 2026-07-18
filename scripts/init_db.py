import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.db.models import Base
from infrastructure.db.session import engine, DATABASE_URL

if __name__ == "__main__":
    print(f"Membuat tabel di: {DATABASE_URL}")
    Base.metadata.create_all(engine)
    print("Semua tabel berhasil dibuat:")
    for table_name in Base.metadata.tables:
        print(f"  - {table_name}")
