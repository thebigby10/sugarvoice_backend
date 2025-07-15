from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "key123"  # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
