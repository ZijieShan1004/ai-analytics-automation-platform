from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Analytics Automation Platform"
    app_env: str = "development"
    app_debug: bool = True
    api_v1_prefix: str = "/api/v1"

    database_url: str

    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120

    upload_dir: str = "/app/storage/uploads"
    max_upload_size_mb: int = 50
    allowed_upload_extensions: str = ".csv,.xlsx,.xls"

    ollama_base_url: str = "http://host.docker.internal:11434"
    ollama_model: str = "qwen2.5:1.5b"
    ollama_timeout_seconds: int = 120
    llm_provider: str = "ollama"

    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Return allowed upload extensions as a set.
    def get_allowed_extensions(self) -> set[str]:
        return {item.strip().lower() for item in self.allowed_upload_extensions.split(",")}


# Return cached application settings.
@lru_cache
def get_settings() -> Settings:
    return Settings()