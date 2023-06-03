import logging.config
import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_DATABASE = os.environ.get("DB_DATABASE", "delivery-service")
    DB_USERNAME = os.environ.get("DB_USERNAME", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", 5432)

    DB_DATABASE_TEST = os.environ.get("DB_DATABASE", "delivery-service-test")
    DB_HOST_TEST = os.environ.get("DB_HOST", "localhost")
    DB_PORT_TEST = os.environ.get("DB_PORT", 5432)

    SQLALCHEMY_DATABASE_URL: str = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    SQLALCHEMY_DATABASE_TEST_URL: str = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_DATABASE_TEST}"
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
            "my.packg": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "__main__": {  # if __name__ == '__main__'
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }


settings = Settings()

logging.config.dictConfig(settings.LOGGING_CONFIG)
