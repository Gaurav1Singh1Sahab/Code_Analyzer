import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    APP_NAME: str = os.getenv("APP_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR")
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()