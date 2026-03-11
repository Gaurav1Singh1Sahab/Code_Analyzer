from fastapi import FastAPI
from app.core.config import settings
from app.db.database import engine, Base

import app.db.models

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0"
)

# print(Base.metadata.tables)

# print(engine.url)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} Running"}