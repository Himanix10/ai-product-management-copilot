import shutil
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config import config

def backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = "data/backups"
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = os.path.join(backup_dir, f"backup_app_{timestamp}.db")
    if os.path.exists(config.DATABASE_PATH):
        shutil.copy(config.DATABASE_PATH, backup_file)
        print(f"Database backed up to {backup_file}")
    else:
        print("Database file not found.")

if __name__ == "__main__":
    backup()