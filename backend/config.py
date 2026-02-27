import os


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID", "")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    MIGRATION_STATE_DIR = os.environ.get("MIGRATION_STATE_DIR", "/tmp/migrations")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    MIGRATION_STATE_DIR = "/tmp/test_migrations"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
