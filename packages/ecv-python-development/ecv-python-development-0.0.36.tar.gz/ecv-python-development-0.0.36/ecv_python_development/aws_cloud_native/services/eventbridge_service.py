from __future__ import annotations

import logging

from mypy_boto3_events import EventBridgeClient
from mypy_boto3_events.type_defs import (
    PutEventsRequestEntryTypeDef,
    PutEventsResponseTypeDef,
)

from .aws_service import AWSService


class EventbridgeService(AWSService):
    client: EventBridgeClient = AWSService.session.client("events", region_name=AWSService.region)  # type: ignore

    @classmethod
    def put_event(
        cls, event: PutEventsRequestEntryTypeDef
    ) -> PutEventsResponseTypeDef | None:
        try:
            return cls.client.put_events(Entries=[event])
        except Exception as e:
            logging.error(e)
            return None
