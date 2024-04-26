from __future__ import annotations

import logging
from typing import Any

from botocore.client import ClientError
from mypy_boto3_ssm import SSMClient

from .aws_service import AWSService
from .exceptions import SSMError


class SSMGateway(AWSService):
    client: SSMClient = AWSService.session.client("ssm", region_name=AWSService.region)  # type: ignore

    @classmethod
    def get_parameter(cls, parameter_name: str) -> str | None:
        try:
            params: dict[str, Any] = {"Name": parameter_name}
            ssm_response = cls.client.get_parameter(**params)

            if "Parameter" not in ssm_response:
                raise SSMError(f"Parameter not found.")

            return str(ssm_response["Parameter"])
        except (ClientError, SSMError) as e:
            logging.error(e)
            return None
