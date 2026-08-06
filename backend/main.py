import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

if __package__ is None:
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root))

from backend.database.db import Base, engine, SessionLocal
from backend.database import models
from backend.database.seeder import seed_db

from backend.routers.workspace import router as workspace_router
from backend.routers.api import router as api_router

# Ensure SQLite schema is created
Base.metadata.create_all(bind=engine)

# Auto-seed sample database records
db = SessionLocal()
try:
    seed_db(db)
finally:
    db.close()

app = FastAPI(
    title="AI Product Management Copilot"
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(workspace_router)
app.include_router(api_router)

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "AI PM Copilot API Server Running"
    }