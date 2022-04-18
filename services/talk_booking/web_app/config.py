import base64
import json
import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError


class ProductionConfig:
    DEBUG: bool = False
    TESTING: bool = False
    APP_ENVIRONMENT: str = "production"
    _SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self._SQLALCHEMY_DATABASE_URI is None:
            secret = get_secret(self.APP_ENVIRONMENT)
            print("SECRET in prod cofig: ", secret)
            self._SQLALCHEMY_DATABASE_URI = secret

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


def get_secret(env: str):
    secret_name = f"db-connection-string-{env}"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "Inv salidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])

    print("SECRET: ", secret)

    return secret
