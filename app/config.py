from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application Info
    PROJECT_NAME: str = "Advanced Asynchronous Backend System (Enterprise Core)"
    VERSION: str = "1.4.2-Prod"
    
    # Infrastructure
    DATABASE_URL: str
    REDIS_URL: str
    
    # Cryptography
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()