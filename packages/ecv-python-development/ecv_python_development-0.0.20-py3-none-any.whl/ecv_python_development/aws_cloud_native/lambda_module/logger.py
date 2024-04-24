from __future__ import annotations

import os
from typing import Any, Optional

from aws_lambda_powertools import Logger

logger = Logger(service=os.environ.get("SERVICE_NAME"), log_uncaught_exceptions=True)


def log(log_name: str, data: Optional[dict[str, Any]] = {}) -> None:
    if data:
        logger.info(log_name, extra=data)  # type: ignore
    else:
        logger.info(log_name)  # type: ignore
