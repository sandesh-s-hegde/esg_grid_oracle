from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    esg_api_key: str = "dev-secret-key"
    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()