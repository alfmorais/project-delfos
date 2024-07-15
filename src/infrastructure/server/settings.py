from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST_AUTH_METHOD: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    PROJECT_TITLE: str
    PROJECT_VERSION: str
    SOURCE_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
