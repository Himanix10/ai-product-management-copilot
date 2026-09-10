import shutil
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config import config

def restore(backup_path: str):
    if os.path.exists(backup_path):
        shutil.copy(backup_path, config.DATABASE_PATH)
        print(f"Restored database from {backup_path}")
    else:
        print("Backup file does not exist.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        restore(sys.argv[1])
    else:
        print("Provide backup path.")