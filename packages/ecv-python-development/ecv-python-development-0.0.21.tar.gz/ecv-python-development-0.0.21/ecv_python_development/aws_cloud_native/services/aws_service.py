from __future__ import annotations

import itertools
import os
from typing import Any

from boto3.session import Session

boto3_session = Session()


class AWSService:
    session = boto3_session
    region: str = os.environ.get("AWS_REGION", "ap-southeast-2")

    @staticmethod
    def grouper(
        iterable: list[Any], n: int, fillvalue: object = None
    ) -> itertools.zip_longest[tuple[Any]]:
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)
