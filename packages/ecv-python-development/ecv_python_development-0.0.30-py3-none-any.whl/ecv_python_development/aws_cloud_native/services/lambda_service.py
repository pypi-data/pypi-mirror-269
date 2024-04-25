from __future__ import annotations

import json
from typing import Any, Literal

from mypy_boto3_lambda import LambdaClient
from mypy_boto3_lambda.type_defs import InvocationResponseTypeDef

from .aws_service import AWSService


class LambdaService(AWSService):
    client: LambdaClient = AWSService.session.client("lambda", region_name=AWSService.region)  # type: ignore

    @classmethod
    def invoke(
        cls,
        function_name: str,
        payload: Any,
        invocation_type: Literal[
            "DryRun", "Event", "RequestResponse"
        ] = "RequestResponse",
    ) -> dict[str, Any]:

        response: InvocationResponseTypeDef = cls.client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            LogType="Tail",
            Payload=payload,
        )

        response_payload = json.loads(response["Payload"].read())

        if response.get("StatusCode") != 200 or not response_payload.get("body", None):
            return {
                "response": {
                    "body": {
                        "error_code": "SERVER_ERROR",
                        "message": "Lambda invocation error: ({})".format(
                            function_name
                        ),
                    },
                    "status_code": 500,
                },
            }

        else:
            return {
                "response": response_payload,
            }
