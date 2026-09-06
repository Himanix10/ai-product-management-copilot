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
    @property
    def OPENROUTER_API_KEYS(self) -> list[str]:
        load_dotenv(override=True)
        return [
            key for key in (
                os.getenv("OPENROUTER_API_KEY", ""),
                os.getenv("OPENROUTER_API_KEY_1", ""),
                os.getenv("OPENROUTER_API_KEY_2", ""),
                os.getenv("OPENROUTER_API_KEY_3", ""),
                os.getenv("OPENROUTER_API_KEY_4", ""),
            ) if key
        ]

    @property
    def OPENROUTER_MODEL(self) -> str:
        load_dotenv(override=True)
        return os.getenv("OPENROUTER_MODEL", "liquid/lfm-2.5-2.6b:free")

    OPENROUTER_BASE_URL: str = os.getenv(
        "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")

os.makedirs(Path(Config.DATABASE_PATH).parent, exist_ok=True)
os.makedirs(Config.LOG_DIR, exist_ok=True)

config = Config()