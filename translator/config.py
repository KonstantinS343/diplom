from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


class DBConfig(BaseSettings):
    host: str
    port: str
    user: str
    password: str
    db: str
    url: str = None

    @model_validator(mode="before")
    @classmethod
    def build_url(cls, values):
        if (
            "host" in values
            and "port" in values
            and "user" in values
            and "password" in values
            and "db" in values
        ):
            values["url"] = (
                f"postgresql+asyncpg://{values['user']}:{values['password']}@"
                f"{values['host']}:{values['port']}/{values['db']}"
            )
        return values

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="POSTGRES_", extra="ignore"
    )


class FastAPIConfig(BaseSettings):
    engine_echo: bool

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="FASTAPI_", extra="ignore"
    )


db_settings = DBConfig()
fastapi_settings = FastAPIConfig()
