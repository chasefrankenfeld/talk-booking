import os
from typing import Optional

import boto3


class ProductionConfig:
    DEBUG: bool = False
    TESTING: bool = False
    APP_ENVIRONMENT: str = "production"
    _SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self._SQLALCHEMY_DATABASE_URI is None:
            self._SQLALCHEMY_DATABASE_URI = boto3.client(
                "secretsmanager"
            ).get_secret_value(SecretId=f"db-connection-string-{self.APP_ENVIRONMENT}")[
                "SecretString"
            ]

        return self._SQLALCHEMY_DATABASE_URI


class DevelopmentConfig(ProductionConfig):
    DEBUG: bool = True
    APP_ENVIRONMENT: str = "development"


class TestConfig(ProductionConfig):
    DEBUG: bool = True
    TESTING: bool = True
    APP_ENVIRONMENT: str = "local"
    _SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return "postgresql://app:talkbooking@postgres:5432/talkbookingtest"


class LocalTestConfig(ProductionConfig):
    DEBUG: bool = True
    APP_ENVIRONMENT: str = "local"
    _SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return "postgresql://app:talkbooking@localhost:5432/talkbooking_test"


class LocalConfig(ProductionConfig):
    DEBUG: bool = True
    APP_ENVIRONMENT: str = "local"
    _SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return "postgresql://app:talkbooking@localhost:5432/talkbooking"


CONFIGS = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestConfig,
    "local_test": LocalTestConfig,
}


def load_config():
    """
    Load config based on environment
    :return:
    """

    return CONFIGS.get(os.getenv("APP_ENVIRONMENT"), LocalConfig)()
