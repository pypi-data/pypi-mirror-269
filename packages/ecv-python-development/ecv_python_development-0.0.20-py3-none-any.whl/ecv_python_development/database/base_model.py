from __future__ import annotations

import os
from typing import Any, Callable, List, Literal, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, StrictBool, StrictFloat, StrictInt, StrictStr

from ._pynamodb.base import (
    PYDANTIC_PYNAMO_MAPPING,
    PynamoDBBaseModel,
    PynamoDBModel,
    UnicodeAttribute,
)

"""
check full documentation for fields at: https://docs.pydantic.dev/latest/concepts/fields/

"""


def field(
    alias: str,
    default: Optional[str] = None,
    default_factory: Optional[Callable[..., Any]] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    validation_alias: Optional[str] = None,
    serialization_alias: Optional[str] = None,
    examples: Optional[List[Any]] = None,
    exclude: Optional[str] = None,
    is_hash_key: Optional[bool] = False,
    is_range_key: Optional[bool] = False,
) -> Any:

    # if serialization_alias is None and alias is not None:
    #     serialization_alias = alias

    if is_hash_key == True:
        json_extra_schema = "__hash_key__"
    elif is_range_key == True:
        json_extra_schema = "__range_key__"

    parameters = {
        key: value
        for key, value in locals().items()
        if value is not None
        and key not in ["parameters", "is_hash_key", "is_range_key"]
    }

    """
    These are the parameters I find to be extremely useful.
    
    I limited the parameters to this for easier readability. 
    
    This custom field is to enforce strict types.
    
    """
    return Field(**parameters, strict=True)


"""
Sample Implementation

from uuid import UUID, uuid4

class User(BaseModel):
    id: UUID = field(default_factory=uuid4)
    name: str = field(default="John Doe", min_length=1, description="name of the User")
    
user = User(name="warren")
print(user.json())

"""


class BaseModel(PydanticBaseModel):
    def __init__(
        self,
        db_type: Literal["dynamodb", "rds", "mongodb"] = "dynamodb",
        table_name: Optional[str] = os.environ.get("METADATA_TABLE", None),
        **data,
    ):
        super().__init__(**data)

        if db_type == "dynamodb":
            self.__PynamoDBModel__: PynamoDBModel = None
            self.__initialize_pynamodb_model__(table_name=table_name)
        else:
            raise Exception("Other database not yet supported")

    def __initialize_pynamodb_model__(
        self, table_name: Optional[str] = None
    ) -> PynamoDBBaseModel:
        attributes: dict = {}

        for field in self.model_fields.values():
            if field.alias not in [
                "__root__",
                "__fields__",
                "__config__",
            ] and field.json_schema_extra["json_extra_schema"] not in [
                "__hash_key__",
                "__range_key__",
            ]:
                attributes[field.alias] = PYDANTIC_PYNAMO_MAPPING.get(
                    field.annotation, UnicodeAttribute
                )()
            elif field.json_schema_extra["json_extra_schema"] in [
                "__hash_key__",
                "__range_key__",
            ]:
                if field.json_schema_extra["json_extra_schema"] == "__hash_key__":
                    attributes[field.alias] = UnicodeAttribute(hash_key=True)
                else:
                    attributes[field.alias] = UnicodeAttribute(range_key=True)

        class_name = f"{self.__class__.__name__}PynamoDBModel"
        PynamoDBBaseModel.Meta.table_name = table_name
        PynamoDBModel = type(class_name, (PynamoDBBaseModel,), attributes)
        self.__PynamoDBModel__ = PynamoDBModel

        return self.__PynamoDBModel__

    def get_pynamodb_model(self) -> PynamoDBBaseModel:
        return self.__PynamoDBModel__(**self.model_dump())
