from __future__ import annotations

import json
import random
import string
from typing import Any

from mypy_boto3_sqs import SQSServiceResource
from mypy_boto3_sqs.type_defs import (
    DeleteMessageBatchResultTypeDef,
    SendMessageBatchResultTypeDef,
    SendMessageResultTypeDef,
)

from .aws_service import AWSService


class SqsService(AWSService):
    client: SQSServiceResource = AWSService.session.resource("sqs", region_name=AWSService.region)  # type: ignore

    @classmethod
    def prepare_messages(
        cls, entries: list[Any], job_type: str
    ) -> list[dict[str, Any]]:
        prepared_messages: list[dict[str, Any]] = []

        for entry in entries:
            letters = string.ascii_lowercase
            queue_item_id = "".join(random.choice(letters) for i in range(16))  # type: ignore

            prepared = {
                "Id": queue_item_id,
                "MessageBody": json.dumps({"job_type": job_type, "data": entry}),
                "DelaySeconds": 2,
            }

            prepared_messages.append(prepared)

        return prepared_messages

    @classmethod
    def send_message(
        cls, queue_name: str, serialized_message: str, message_execution_delay: int = 0
    ) -> SendMessageResultTypeDef:

        queue = cls.client.get_queue_by_name(QueueName=queue_name)

        return queue.send_message(
            MessageBody=serialized_message, DelaySeconds=message_execution_delay
        )

    @classmethod
    def batch_send_message(
        cls, queue_name: str, entries: list[Any]
    ) -> SendMessageBatchResultTypeDef:
        queue = cls.client.get_queue_by_name(QueueName=queue_name)

        return queue.send_messages(Entries=entries)

    @classmethod
    def group_batch_send_message(
        cls, queue_name: str, entries: list[Any], fifo: bool = False
    ) -> list[Any]:
        queue = cls.client.get_queue_by_name(QueueName=queue_name)

        responses: list[Any] = []
        grouped_entries = list(cls.grouper(entries, 10))

        letters = string.ascii_lowercase
        group_id = "".join(random.choice(letters) for i in range(16))  # type: ignore

        for index, group in enumerate(grouped_entries):
            batch_entries = list(filter(None.__ne__, group))

            if fifo:
                for index, group_item in enumerate(batch_entries):
                    if index <= int((len(grouped_entries) - 1) / 2):
                        group_item["MessageGroupId"] = group_id + "01"
                    else:
                        group_item["MessageGroupId"] = group_id + "02"

                    if "DelaySeconds" in group_item:
                        del group_item["DelaySeconds"]

            sqs_response: SendMessageBatchResultTypeDef = queue.send_messages(
                Entries=batch_entries
            )

            responses.append(sqs_response)

        return responses

    @classmethod
    def delete_message(
        cls, queue_name: str, entries: list[Any]
    ) -> DeleteMessageBatchResultTypeDef:
        queue = cls.client.get_queue_by_name(QueueName=queue_name)

        responses: DeleteMessageBatchResultTypeDef = queue.delete_messages(
            Entries=entries
        )

        return responses
