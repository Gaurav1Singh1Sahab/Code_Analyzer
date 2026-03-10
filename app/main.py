from fastapi import FastAPI
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    description=f"{settings.APP_NAME} is a code analyzer AI that analyzes code and provides insights",
    version="1.0.0",
    
)

@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running"}