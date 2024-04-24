from __future__ import annotations

from typing import Any

import requests


def send_get_request(
    url: str, headers: dict[Any, Any], payload: dict[Any, Any] = {}
) -> dict[str, Any]:
    response = requests.request(
        "GET", url, headers=headers, data=payload, params=payload
    )
    return {
        "code": response.status_code,
        "reason": response.reason,
        "body": response.json(),
    }


def send_post_request(
    url: str, headers: dict[Any, Any], payload: dict[Any, Any]
) -> dict[str, Any]:
    response = requests.request("POST", url, headers=headers, data=payload)
    return {
        "code": response.status_code,
        "reason": response.reason,
        "body": response.json(),
    }
