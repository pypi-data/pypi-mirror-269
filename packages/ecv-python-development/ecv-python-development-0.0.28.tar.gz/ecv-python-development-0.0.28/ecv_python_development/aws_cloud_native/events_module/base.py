from __future__ import absolute_import, annotations

import json
import os
from typing import Any
from uuid import uuid4

import jsonpickle  # type: ignore

from ...helpers.datetime.standard import DateTime
from ..lambda_module.logger import log
from ..lambda_module.tracer import tracer
from ..services.eventbridge_service import (
    EventbridgeService,
    PutEventsRequestEntryTypeDef,
)
from ..services.s3_service import S3Service

jsonpickle.set_encoder_options("simplejson", use_decimal=True, sort_keys=True)  # type: ignore
jsonpickle.set_preferred_backend("simplejson")  # type: ignore


class BaseEvent:
    event_name: str
    event_bus: str = os.environ.get("PROJECT_BUS", "")
    function: str = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "")
    service: str = os.environ.get("SERVICE_NAME", "")
    project: str = os.environ.get("PROJECT_NAME", "")
    environment: str = os.environ.get("ENVIRONMENT", "")
    bucket: str = os.environ.get("PROJECT_S3", "")

    @classmethod
    @tracer.capture_method
    def emit(cls, content: Any):
        event_name = cls.event_name

        source: str = (
            "{env}.{project}".format(env=cls.environment, project=cls.project)
            .lower()
            .replace(" ", "_")
        )

        payload = {
            "emitter": cls.function,
            "service": cls.service,
            "event_name": event_name,
            "event_type": "raw",
            "event": content,
            "created_at": DateTime(),
        }
        string_payload: str = jsonpickle.encode(  # type: ignore
            payload, unpicklable=False, make_refs=False, use_decimal=True
        )

        event: PutEventsRequestEntryTypeDef = {
            "Source": source,
            "DetailType": event_name,
            # Has to be small, we're imitating the EventBridge event
            "Detail": string_payload,
            "EventBusName": cls.event_bus,
        }

        log("emitting_event", data=dict(event))

        # Determine if beyond size
        event_size: int = len(string_payload)
        if event_size > 200000:
            log("event_too_large_saving_to_s3")
            current_date = DateTime.get_current_date().split("-")
            current_time = DateTime.get_current_time()
            file_key = (
                "events/{event_name}/{year}/{month}/{day}/{time}_{uuid}.json".format(
                    event_name=event_name,
                    year=current_date[0],
                    month=current_date[1],
                    day=current_date[2],
                    time=current_time,
                    uuid=str(uuid4()).split("-")[0],
                )
            )

            S3Service.put_object(
                body=string_payload.encode("utf-8"),
                bucket=cls.bucket,
                key=file_key,
            )
            event["Detail"] = json.dumps({"event_type": "json", "file_key": file_key})
            log("event_saved", data={"file_key": file_key})

        EventbridgeService.put_event(event)

        log("event_emitted", data=dict(event))
