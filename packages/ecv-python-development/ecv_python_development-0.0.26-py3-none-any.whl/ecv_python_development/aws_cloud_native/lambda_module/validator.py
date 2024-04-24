from __future__ import annotations

import json
from typing import Any, Callable, Type

from aws_lambda_powertools.middleware_factory import (
    lambda_handler_decorator,  # type: ignore
)
from pydantic import BaseModel, ValidationError

from .exceptions import PydanticBaseModelException, RequestValidationException
from .handler import LambdaContextTypeDef, LambdaEventTypeDef, app
from .logger import log
from .response import APIGatewayResponse


@lambda_handler_decorator
def validate_function_source(
    handler: Callable[..., APIGatewayResponse],
    event: LambdaEventTypeDef,
    context: LambdaContextTypeDef,
) -> APIGatewayResponse | dict[Any, Any]:
    if _skip_warmup_call(event):
        return {}

    response = handler(event, context)
    print("LAMBDA_HANDLER_RESPONSE: ", response)
    return response


@lambda_handler_decorator
def validate_web_request(
    handler: Callable[..., APIGatewayResponse],
    event: LambdaEventTypeDef,
    context: LambdaContextTypeDef,
    model: Type[BaseModel],
) -> APIGatewayResponse | dict[Any, Any]:
    if _skip_warmup_call(event):
        return {}

    if not issubclass(model, BaseModel):  # type: ignore
        raise PydanticBaseModelException

    body: dict[Any, Any] = {}
    if event["body"]:
        body = json.loads(event["body"])
    if event["queryStringParameters"]:
        body = {**body, **event["queryStringParameters"]}
    if event["pathParameters"]:
        body = {**body, **event["pathParameters"]}

    log("UNVALIDATED_BODY", data=body)
    result = _validate_data(body, model_class=model)

    if not isinstance(result, BaseModel):
        return {
            "body": json.dumps(
                {
                    "error": {
                        "code": RequestValidationException.ERROR_CODE,
                        "message": RequestValidationException.ERROR_MESSAGE,
                        "error_details": _construct_validation_error_message(result),
                    }
                },
                default=str,
            ),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Header": "*",
            },
            "status_code": RequestValidationException.STATUS_CODE,
        }

    app.validated_body = result.model_dump()

    response = handler(event, context)
    print("LAMBDA_HANDLER_RESPONSE: ", response)

    return response


def _skip_warmup_call(event: dict[Any, Any]) -> bool:
    skip = False
    if event.get("source") == "serverless-plugin-warmup":
        log("LAMBDA_WARMER_INVOCATION")
        skip = True

    return skip


def _validate_data(
    data: dict[str, Any], model_class: Type[BaseModel]
) -> BaseModel | dict[Any, Any]:
    try:
        validated_data = model_class.model_validate(data)
        return validated_data
    except ValidationError as e:
        errors: dict[Any, Any] = {}
        for error in e.errors():
            errors[error["loc"][0]] = error["msg"]
        return errors


def _construct_validation_error_message(
    validated_data: dict[Any, Any]
) -> list[dict[str, Any]]:
    error_message_list: list[dict[Any, Any]] = []
    for field, error in validated_data.items():
        temp_dict: dict[Any, Any] = {}
        temp_dict["field"] = field
        temp_dict["error"] = error
        error_message_list.append(temp_dict)

    return error_message_list
