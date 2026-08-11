from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn, SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='forbid',
    )

    # Database
    DATABASE_URL: PostgresDsn

    # JWT
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Redis
    REDIS_URL: RedisDsn

    # Celery
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn

    # AI Service
    AI_SERVICE_API_KEY: SecretStr
    AI_SERVICE_URL: str

settings = Settings()
