from __future__ import annotations

import logging

from botocore.client import ClientError
from mypy_boto3_secretsmanager import SecretsManagerClient

from .aws_service import AWSService


class SecretsManager(AWSService):
    client: SecretsManagerClient = AWSService.session.client(service_name="secretsmanager", region_name=AWSService.region)  # type: ignore

    @classmethod
    def get_secret(cls, secret_name: str) -> str | None:
        try:
            get_secret_value_response = cls.client.get_secret_value(
                SecretId=secret_name
            )
            # Decrypts secret using the associated KMS key.
            secret = get_secret_value_response["SecretString"]
            return secret
        except ClientError as e:
            logging.error(e)
            return None
