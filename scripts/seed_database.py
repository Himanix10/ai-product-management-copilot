import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from create_db import build_database

if __name__ == "__main__":
    build_database()