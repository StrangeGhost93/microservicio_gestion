import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    SECRET_KEY = os.getenv("GESTION_SECRET_KEY", "change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    API_TITLE = "Gestion Academica API"
    API_VERSION = "v1"
    DEFAULT_PAGE_SIZE = 20
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 60
    CACHE_REDIS_URL = os.getenv("GESTION_REDIS_URL", "redis://localhost:6379/0")
    RATELIMIT_DEFAULT = os.getenv("GESTION_RATE_LIMIT", "60 per minute")
    RATELIMIT_STORAGE_URI = CACHE_REDIS_URL
    DOCUMENTACION_BASE_URL = os.getenv("DOCUMENTACION_BASE_URL", "http://localhost:5001")
    DOCUMENTACION_TIMEOUT = float(os.getenv("DOCUMENTACION_TIMEOUT", "3"))

    @staticmethod
    def init_app(app):
        """Hook para configurar logs u otras extensiones."""
        app.logger.setLevel(os.getenv("GESTION_LOG_LEVEL", "INFO"))


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "GESTION_DEV_DATABASE_URI",
        f"sqlite:///{BASE_DIR / 'gestion_dev.db'}",
    )


class TestingConfig(BaseConfig):
    TESTING = True
    CACHE_TYPE = "SimpleCache"
    RATELIMIT_STORAGE_URI = "memory://"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "GESTION_TEST_DATABASE_URI",
        "sqlite:///:memory:",
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("GESTION_DATABASE_URI")


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
