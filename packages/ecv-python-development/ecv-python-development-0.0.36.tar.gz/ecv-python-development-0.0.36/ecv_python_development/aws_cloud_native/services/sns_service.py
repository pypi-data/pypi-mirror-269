from __future__ import annotations

from mypy_boto3_sns import SNSClient
from mypy_boto3_sns.type_defs import PublishResponseTypeDef

from .aws_service import AWSService


class SnsService(AWSService):
    client: SNSClient = AWSService.session.client("sns", region_name=AWSService.region)  # type: ignore

    @classmethod
    def publish_message(
        cls, message: str, subject: str, topic_arn: str
    ) -> PublishResponseTypeDef:

        response = cls.client.publish(
            TopicArn=topic_arn, Subject=subject, Message=message
        )

        return response
