from __future__ import annotations

import os
from typing import Any, Callable, Dict, List

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import CORSConfig
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from .logger import logger
from .metrics import metrics
from .tracer import tracer

LambdaContextTypeDef = LambdaContext
LambdaEventTypeDef = Dict[Any, Any]


class ECVAPIGatewayRestResolver(APIGatewayRestResolver):
    def __init__(
        self,
        cors: CORSConfig | None = None,
        debug: bool | None = None,
        serializer: Callable[[Dict[Any, Any]], str] | None = None,
        strip_prefixes: List[str] | None = None,
    ) -> None:
        self.validated_body: dict[Any, Any] = {}
        super().__init__(cors, debug, serializer, strip_prefixes)  # type: ignore


app = ECVAPIGatewayRestResolver(debug=(os.environ.get("ENVIRONMENT") != "prod"))


@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST,
    log_event=True,
    clear_state=True,
)
@tracer.capture_lambda_handler  # type: ignore
@metrics.log_metrics(raise_on_empty_metrics=False)  # type: ignore
def start_handler(event: LambdaEventTypeDef, context: LambdaContext) -> dict[str, Any]:
    res = app.resolve(event, context)  # type: ignore
    return res


def spawn_handler(event: LambdaEventTypeDef, context: LambdaContext) -> dict[str, Any]:
    return start_handler(event, context)  # type: ignore
