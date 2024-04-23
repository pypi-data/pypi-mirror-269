"""

This is ECV's Python AWS Services Module

"""

__version__ = "0.0.1"
__license__ = "MIT"
__author__ = "Warren Ezra Bruce Jaudian <warren.jaudian@ecloudvalley.com>"

from . import (
    cognito_service,
    dynamodb_service,
    eventbridge_service,
    kms_service,
    lambda_service,
    s3_service,
    secretsmanager_service,
    ses_service,
    sns_service,
    sqs_service,
    ssm_service,
)

__all__ = [
    "cognito_service",
    "dynamodb_service",
    "eventbridge_service",
    "kms_service",
    "lambda_service",
    "s3_service",
    "secretsmanager_service",
    "ses_service",
    "sns_service",
    "sqs_service",
    "ssm_service",
]
