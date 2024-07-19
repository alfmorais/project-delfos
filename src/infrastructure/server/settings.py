from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    POSTGRES_DB: str
    POSTGRES_HOST_AUTH_METHOD: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    PROJECT_TITLE: str
    PROJECT_VERSION: str
    SOURCE_DATABASE_URL: str


settings = Settings()
