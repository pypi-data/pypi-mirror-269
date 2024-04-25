from __future__ import annotations

import json
from typing import Any

from aws_lambda_powertools.event_handler import Response, content_types

from .exceptions import CustomException

APIGatewayResponse = Response


def _cors_response(code: int, body: Any) -> Response:
    return Response(
        status_code=code,
        content_type=content_types.APPLICATION_JSON,
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Header": "*",
        },
        body=body,
    )


def ErrorResponse(error: CustomException) -> Response:
    err = {
        "code": error.ERROR_CODE,
        "message": error.ERROR_MESSAGE,
    }

    if hasattr(error, "ERROR_DETAILS"):
        err["error_details"] = error.ERROR_DETAILS

    return _cors_response(
        code=error.STATUS_CODE,
        body=json.dumps({"error": err}),
    )


def ExceptionResponse(error: Exception) -> Response:
    err = {"code": 500, "message": "SERVER_ERROR", "error_details": str(error)}

    return _cors_response(
        code=500,
        body=json.dumps({"error": err}),
    )


def SuccessResponse(
    data: Any, status_code: int = 200, **other_data: dict[Any, Any]
) -> Response:
    response = {
        "status": "success",
        "status_code": status_code,
        "data": data,
        **other_data,
    }

    return _cors_response(
        code=200,
        body=json.dumps(response),
    )
