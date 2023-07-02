import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_DATABASE = os.environ.get("DB_DATABASE", "delivery-service")
    DB_USERNAME = os.environ.get("DB_USERNAME", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", 5432)

    DB_DATABASE_TEST = os.environ.get("DB_DATABASE_TEST", "delivery-service-test")
    DB_HOST_TEST = os.environ.get("DB_HOST_TEST", "localhost")
    DB_PORT_TEST = os.environ.get("DB_PORT_TEST", 5432)

    SQLALCHEMY_DATABASE_URL: str = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    SQLALCHEMY_DATABASE_TEST_URL: str = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_DATABASE_TEST}"

    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
    )


settings = Settings()
