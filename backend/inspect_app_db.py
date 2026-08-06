import sqlite3
from pathlib import Path

path = Path(__file__).resolve().parent / "database" / "app.db"
print("DB file:", path)
print("Exists:", path.exists())

if path.exists():
    with sqlite3.connect(path) as db:
        cur = db.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        print("Tables:", tables)
        for table, in tables:
            cur.execute(f"SELECT count(*) FROM {table};")
            print(f"{table}:", cur.fetchone()[0])
