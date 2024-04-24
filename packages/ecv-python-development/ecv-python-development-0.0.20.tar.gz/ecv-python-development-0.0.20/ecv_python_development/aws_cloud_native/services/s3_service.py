from __future__ import annotations

import logging
from typing import Any

from botocore.exceptions import ClientError
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import (
    BlobTypeDef,
    DeleteObjectOutputTypeDef,
    GetObjectOutputTypeDef,
)

from .aws_service import AWSService


class S3Service(AWSService):
    client: S3Client = AWSService.session.client("s3", region_name=AWSService.region)  # type: ignore

    @classmethod
    def download_file(cls, bucket: str, key: str) -> GetObjectOutputTypeDef:
        return cls.client.get_object(Bucket=bucket, Key=key)

    @classmethod
    def delete_file(cls, bucket: str, key: str) -> DeleteObjectOutputTypeDef:
        return cls.client.delete_object(Bucket=bucket, Key=key)

    @classmethod
    def put_object(
        cls, body: BlobTypeDef, bucket: str, key: str
    ) -> dict[str, Any] | None:
        try:
            response = cls.client.put_object(
                Body=body,
                Bucket=bucket,
                Key=key,
            )
            return {
                "sent": True,
                "bucket_name": bucket,
                "response": response,
                "object_name": key,
            }
        except ClientError as e:
            logging.error(e)
            return None

    @classmethod
    def upload_file(
        cls, filename: str, bucket_name: str, object_name: str | None = None
    ) -> dict[str, Any] | None:
        try:
            if object_name is None:
                object_name = filename

            cls.client.upload_file(filename, bucket_name, object_name)
            return {
                "sent": True,
                "bucket_name": bucket_name,
                "object_name": object_name,
            }
        except ClientError as e:
            logging.error(e)
            return None

    @classmethod
    def generate_presigned_url(
        cls, bucket_name: str, object_name: str, expiry_seconds: int
    ) -> str | None:
        try:
            response = cls.client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket_name, "Key": object_name},
                ExpiresIn=expiry_seconds,
            )
            return response
        except ClientError as e:
            logging.error(e)
            return None
