from fastapi import FastAPI

from database.db import Base, engine
from database import models

from routers.workspace import router as workspace_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Product Management Copilot"
)

app.include_router(workspace_router)


@app.get("/")
def root():
    return {
        "message": "Backend Running"
    }