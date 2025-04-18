from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


class TranslatorConfig(BaseSettings):
    service_api: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="TRANSLATOR_", extra="ignore"
    )


translator_settings = TranslatorConfig()
