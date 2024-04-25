from __future__ import annotations

from typing import Any

from mypy_boto3_ses import SESClient
from mypy_boto3_ses.type_defs import SendEmailResponseTypeDef

from .aws_service import AWSService


class SesService(AWSService):
    client: SESClient = AWSService.session.client("ses", region_name=AWSService.region)  # type: ignore

    @classmethod
    def send_html_email(
        cls,
        email_subject: str,
        html_email_content: str,
        recipients: list[Any],
        from_email: str,
    ) -> SendEmailResponseTypeDef:

        CHARSET = "UTF-8"

        response = cls.client.send_email(
            Destination={"ToAddresses": recipients},
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": html_email_content,
                    }
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": email_subject,
                },
            },
            Source=from_email,
        )

        return response
