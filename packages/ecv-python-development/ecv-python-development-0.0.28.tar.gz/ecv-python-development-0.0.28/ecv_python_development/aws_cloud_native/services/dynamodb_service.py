from __future__ import annotations

from typing import Any, Optional

from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.type_defs import (
    DeleteItemOutputTableTypeDef,
    GetItemOutputTableTypeDef,
    PutItemOutputTableTypeDef,
    QueryOutputTableTypeDef,
    ScanOutputTableTypeDef,
    TableAttributeValueTypeDef,
)

from .aws_service import AWSService
from .exceptions import MissingItemsException


class DynamodbService(AWSService):
    client: DynamoDBServiceResource = AWSService.session.resource("dynamodb", region_name=AWSService.region)  # type: ignore

    @classmethod
    def upsert(
        cls, table_name: str, mapping_data: list[Any], primary_keys: list[str]
    ) -> None:
        table = cls.client.Table(table_name)

        for group in cls.grouper(mapping_data, 100):
            batch_entries = list(filter(None.__ne__, group))
            with table.batch_writer(overwrite_by_pkeys=primary_keys) as batch:
                for entry in batch_entries:
                    batch.put_item(Item=entry)

    @classmethod
    def scan_table(
        cls,
        table_name: str,
        last_evaluated_key: Optional[dict[str, TableAttributeValueTypeDef]] = None,
    ) -> dict[str, Any]:
        table = cls.client.Table(table_name)
        items: list[Any] = []
        response: ScanOutputTableTypeDef

        if last_evaluated_key is not None:
            response = table.scan(ExclusiveStartKey=last_evaluated_key)
        else:
            response = table.scan()

        items.extend(response["Items"])

        if "Items" not in response:
            raise MissingItemsException(f"No objects for this table {table_name}")

        if "LastEvaluatedKey" not in response:
            response["LastEvaluatedKey"] = None

        while ("LastEvaluatedKey" in response) and (
            response["LastEvaluatedKey"] != None
        ):
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])

            items.extend(response["Items"])

        return {"items": items, "last_evaluated_key": response["LastEvaluatedKey"]}

    @classmethod
    def count_entries_by_scan(cls, table_name: str):
        table = cls.client.Table(table_name)
        count = 0

        response: ScanOutputTableTypeDef = table.scan()

        if "Items" not in response:
            raise MissingItemsException(f"No objects for this table {table_name}")

        count += len(response["Items"])

        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])

            count += len(response["Items"])

        return count

    @classmethod
    def delete_item(
        cls, table_name: str, primary_key: dict[str, Any]
    ) -> DeleteItemOutputTableTypeDef:
        table = cls.client.Table(table_name)

        response = table.delete_item(
            Key=primary_key,
        )

        return response

    @classmethod
    def get_item_by_primary_key(
        cls, table_name: str, primary_key: dict[str, Any]
    ) -> dict[str, TableAttributeValueTypeDef] | None:
        table = cls.client.Table(table_name)

        response = table.get_item(Key=primary_key)

        if "Item" not in response:
            return None

        return response["Item"]

    @classmethod
    def query_by_partition_key(
        cls, table_name: str, partition_key_name: str, partition_key_query_value: str
    ) -> list[dict[str, TableAttributeValueTypeDef]]:

        table = cls.client.Table(table_name)

        response: QueryOutputTableTypeDef = table.query(
            KeyConditionExpression=Key(partition_key_name).eq(partition_key_query_value)
        )

        return response["Items"]

    @classmethod
    def batch_upsert(
        cls, table_name: str, mapping_data: list[Any], primary_keys: list[str]
    ) -> None:
        table = cls.client.Table(table_name)

        for group in cls.grouper(mapping_data, 100):
            batch_entries = list(filter(None.__ne__, group))

            with table.batch_writer(overwrite_by_pkeys=primary_keys) as batch:
                for entry in batch_entries:
                    batch.put_item(Item=entry)

    @classmethod
    def create_item(
        cls, table_name: str, payload: dict[str, TableAttributeValueTypeDef]
    ) -> PutItemOutputTableTypeDef:
        table = cls.client.Table(table_name)

        result = table.put_item(Item=payload)

        return result

    @classmethod
    def query_all_by_global_secondary_index(
        cls,
        table_name: str,
        partition_key_name: str,
        partition_key_query_value: str,
        global_secondary_index_name: str,
        selected_attributes: str,
        expression_attributes: dict[str, str],
    ) -> list[dict[str, TableAttributeValueTypeDef]]:
        table = cls.client.Table(table_name)

        items: list[dict[str, TableAttributeValueTypeDef]] = []

        response: QueryOutputTableTypeDef = table.query(
            IndexName=global_secondary_index_name,
            KeyConditionExpression=Key(partition_key_name).eq(
                partition_key_query_value
            ),
            ScanIndexForward=False,
            ProjectionExpression=selected_attributes,
            ExpressionAttributeNames=expression_attributes,
        )

        items.extend(response["Items"])

        while "LastEvaluatedKey" in response:
            response = table.query(
                IndexName=global_secondary_index_name,
                KeyConditionExpression=Key(partition_key_name).eq(
                    partition_key_query_value
                ),
                ScanIndexForward=False,
                ExclusiveStartKey=response["LastEvaluatedKey"],
                ProjectionExpression=selected_attributes,
                ExpressionAttributeNames=expression_attributes,
            )

            items.extend(response["Items"])

        return items

    @classmethod
    def query_by_global_secondary_index(
        cls,
        table_name: str,
        partition_key_name: str,
        partition_key_query_value: str,
        global_secondary_index_name: str,
    ) -> list[dict[str, TableAttributeValueTypeDef]]:
        table = cls.client.Table(table_name)
        items: list[dict[str, TableAttributeValueTypeDef]] = []
        response: QueryOutputTableTypeDef = table.query(
            IndexName=global_secondary_index_name,
            KeyConditionExpression=Key(partition_key_name).eq(
                partition_key_query_value
            ),
        )

        items.extend(response["Items"])

        while "LastEvaluatedKey" in response:
            response = table.query(
                IndexName=global_secondary_index_name,
                KeyConditionExpression=Key(partition_key_name).eq(
                    partition_key_query_value
                ),
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )

            items.extend(response["Items"])

        return items

    @classmethod
    def get_item_by_composite_key(
        cls,
        table_name: str,
        partition_key_name: str,
        partition_key_query_value: str,
        sort_key_name: str,
        sort_key_query_value: str,
    ) -> list[dict[str, TableAttributeValueTypeDef]] | None:
        table = cls.client.Table(table_name)

        response: GetItemOutputTableTypeDef = table.get_item(
            Key={
                f"{partition_key_name}": partition_key_query_value,
                f"{sort_key_name}": sort_key_query_value,
            }
        )

        if "Item" not in response:
            return None

        return [response["Item"]]
