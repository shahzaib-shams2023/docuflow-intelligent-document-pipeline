from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "DocuFlow Intelligent Document & Invoice Processing Pipeline"
    host: str = "0.0.0.0"
    port: int = 8003
    environment: str = "development"

    math_tolerance_cents: float = 0.05
    auto_approve_confidence_threshold: float = 0.90

    llm_api_key: Optional[str] = None
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

