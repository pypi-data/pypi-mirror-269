import os

from pynamodb.attributes import (
    BooleanAttribute,
    MapAttribute,
    NumberAttribute,
    UnicodeAttribute,
)
from pynamodb.models import Model as PynamoDBModel

PYDANTIC_PYNAMO_MAPPING = {
    str: UnicodeAttribute,
    int: NumberAttribute,
    float: NumberAttribute,
    bool: BooleanAttribute,
    dict: MapAttribute,
}


class PynamoDBBaseModel(PynamoDBModel):
    class Meta:
        table_name = ""
        region = os.environ.get("AWS_REGION", "us-east-1")
