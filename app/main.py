from fastapi import FastAPI
from app.core.config import settings
from app.db.database import engine, Base

# load models
import app.db.models

# import routers
from app.api.auth import router as auth_router

from app.api.projects import router as project_router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0"
)

# create database tables
Base.metadata.create_all(bind=engine)

# include auth routes
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} Running"}


app.include_router(
    project_router,
    prefix="/api",
    tags=["Projects"]
)