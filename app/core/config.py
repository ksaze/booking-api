from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Fitness Studio Booking API"
    API_V1_STR: str = "/api/v1"

    # --- Auth / JWT ---
    SECRET_KEY: str = "dev-secret-key-change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- Database ---
    DATABASE_URL: str = "sqlite:///./fitness_studio.db"

    # --- Celery ---
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # --- Timezone (class times are canonically stored in IST) ---
    TIMEZONE: str = "Asia/Kolkata"
    model_config = SettingsConfigDict(model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    ))


settings = Settings()
