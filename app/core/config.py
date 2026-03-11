import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Code Analyzer")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")

    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )

    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://localhost/code_analyzer"
    )


settings = Settings()