import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    APP_NAME: str = os.getenv("APP_NAME", "AI Product Manager Copilot")
    ENV: str = os.getenv("ENV", "development")
    DATABASE_PATH: str = str(BASE_DIR / os.getenv("DATABASE_PATH", "data/app.db"))
    LOG_DIR: str = str(BASE_DIR / "logs")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")

os.makedirs(Path(Config.DATABASE_PATH).parent, exist_ok=True)
os.makedirs(Config.LOG_DIR, exist_ok=True)

config = Config()