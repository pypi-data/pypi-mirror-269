from __future__ import annotations

import base64
import os

import aws_encryption_sdk  # type: ignore
from aws_encryption_sdk.identifiers import CommitmentPolicy  # type: ignore
from mypy_boto3_kms import KMSClient

from .aws_service import AWSService


class KMSService(AWSService):

    key_id = os.environ["KEY_ID"]
    kms_client: KMSClient = AWSService.session.client(  # type: ignore
        "kms", region_name=AWSService.region
    )

    @classmethod
    def decrypt(cls, code: str) -> str:
        client = aws_encryption_sdk.EncryptionSDKClient(
            commitment_policy=CommitmentPolicy.FORBID_ENCRYPT_ALLOW_DECRYPT
        )
        kms_key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(
            key_ids=[cls.key_id]
        )

        decrypted_plaintext, decryptor_header = client.decrypt(  # type: ignore
            source=bytes(base64.b64decode(code)), key_provider=kms_key_provider
        )

        return decrypted_plaintext.decode("utf-8")
