# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # DB: safe default for dev; override with env on Vercel
    DATABASE_URL: str = Field(default="sqlite:///./dev.db")

    # Auth / JWT – give dev defaults so missing envs don’t crash boot
    JWT_SECRET: str = Field(default="dev-secret")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    # Allow extra envs without failing, and load local .env if present
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
