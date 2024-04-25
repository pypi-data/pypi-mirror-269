from __future__ import annotations

import logging
import os
import random
import string
from typing import Any

from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from mypy_boto3_cognito_idp.type_defs import (
    AdminCreateUserResponseTypeDef,
    AdminGetUserResponseTypeDef,
    EmptyResponseMetadataTypeDef,
)

from .aws_service import AWSService


class CognitoService(AWSService):
    cognito_arn: str = os.getenv("COGNITO_USERS_ARN", "")
    userpool_id: str = cognito_arn.split("/")[1]

    client: CognitoIdentityProviderClient = AWSService.session.client(  # type: ignore
        "cognito-idp", region_name=AWSService.region
    )

    @classmethod
    def create_cognito_user(
        cls,
        user_attributes: list[Any],
        username: str,
        temporary_password: str,
        client_metadata: dict[Any, Any],
    ) -> Any | dict[Any, Any]:

        response: AdminCreateUserResponseTypeDef = cls.client.admin_create_user(
            UserPoolId=cls.userpool_id,
            Username=username,
            UserAttributes=user_attributes,
            ClientMetadata=client_metadata,
            TemporaryPassword=temporary_password,
            ForceAliasCreation=False,
            MessageAction="SUPPRESS",
        )

        logging.info("cognito_create_user_response", extra=dict(response))
        return response

    @classmethod
    def resend_temporary_password(
        cls, temporary_password: str, username: str
    ) -> dict[str, Any] | None:

        try:
            response = cls.client.admin_set_user_password(
                UserPoolId=cls.userpool_id,
                Username=username,
                Password=temporary_password,
            )
            logging.info("cognito_resend_password", extra=response)
        except Exception as e:
            print(str(e))
            response = None

        return response

    @classmethod
    def update_cognito_user_attributes(
        cls, username: str, user_attributes: list[Any]
    ) -> dict[str, Any] | None:

        try:
            response = cls.client.admin_update_user_attributes(
                UserPoolId=cls.userpool_id,
                Username=username,
                UserAttributes=user_attributes,
            )
            logging.info("cognito_update_response", extra=response)
        except Exception as e:
            print(str(e))
            response = None

        return response

    @classmethod
    def enable_cognito_user(cls, username: str) -> dict[str, Any] | None:
        try:
            response = cls.client.admin_enable_user(
                UserPoolId=cls.userpool_id, Username=username
            )
        except Exception as e:
            print(str(e))
            response = None

        return response

    @classmethod
    def disable_cognito_user(cls, username: str) -> dict[str, Any] | None:
        try:
            response = cls.client.admin_disable_user(
                UserPoolId=cls.userpool_id, Username=username
            )
        except Exception as e:
            print(str(e))
            response = None

        return response

    @classmethod
    def reset_user_password(cls, username: str) -> str:
        characters = string.ascii_letters + string.digits
        password = "".join(random.choice(characters) for i in range(8))  # type: ignore

        cls.client.admin_set_user_password(
            UserPoolId=cls.userpool_id,
            Username=username,
            Password=password,
            Permanent=False,
        )

        return password

    @classmethod
    def set_user_password(cls, username: str, password: str) -> dict[str, Any]:

        return cls.client.admin_set_user_password(
            UserPoolId=cls.userpool_id,
            Username=username,
            Password=password,
            Permanent=True,
        )

    @classmethod
    def get_cognito_user(cls, username: str) -> AdminGetUserResponseTypeDef | None:
        try:
            response = cls.client.admin_get_user(
                UserPoolId=cls.userpool_id, Username=username
            )
        except Exception as e:
            print(str(e))
            response = None

        return response

    @classmethod
    def delete_cognito_user(cls, username: str) -> EmptyResponseMetadataTypeDef | None:
        try:
            response = cls.client.admin_delete_user(
                UserPoolId=cls.userpool_id, Username=username
            )
            print("delete_cognito_user: ", username)
        except Exception as e:
            print(str(e))
            response = None

        return response
