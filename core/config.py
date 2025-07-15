from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./diabetes_tracker.db"
    ALLOWED_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
