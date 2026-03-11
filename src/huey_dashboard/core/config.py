from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    HUEY_NAME: str = "huey"
    BIND_SIGNALS: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
