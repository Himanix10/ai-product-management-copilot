import sqlite3
from pathlib import Path

path = Path(__file__).resolve().parent / "database" / "app.db"
print("DB file:", path)
print("Exists:", path.exists())

if not path.exists():
    raise SystemExit("Database file not found")

with sqlite3.connect(path) as conn:
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(prds);")
    print("PRD schema:", cur.fetchall())
    cur.execute("SELECT * FROM prds LIMIT 10;")
    rows = cur.fetchall()
    print(f"PRD rows: {len(rows)}")
    for row in rows:
        print(row)
