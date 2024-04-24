from __future__ import annotations

import os
from typing import Any, Callable, ClassVar, List, Literal, Optional, Pattern

from pydantic import BaseModel as PydanticBaseModel
from pydantic import (
    Field,
    PrivateAttr,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    create_model,
)

from ..helpers.datetime import DateTime
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
    default: Optional[str] = None,
    default_factory: Optional[Callable[..., Any]] = None,
    alias: Optional[str] = None,
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
    frozen: Optional[bool] = False,
    exclude: Optional[bool] = False,
    pattern: Optional[Pattern[str]] = None,
    is_hash_key: Optional[bool] = False,
    is_range_key: Optional[bool] = False,
    metadata: Optional[dict] = None,
) -> Any:

    json_extra_schema = {}

    if is_hash_key == True:
        json_extra_schema["__hash_key__"] = True
    elif is_range_key == True:
        json_extra_schema["__range_key__"] = True

    if metadata is not None:
        json_extra_schema = {**json_extra_schema, **metadata}

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
    created_at: str = field(
        default_factory=DateTime.get_current_datetime,
        alias="created_at",
        frozen=True,
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
    )
    created_by: str = field(frozen=True)
    updated_at: str = field(
        default_factory=DateTime.get_current_datetime,
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
    )
    updated_by: str = field()

    def __init__(
        self,
        db_type: Literal["dynamodb", "rds", "mongodb", "temporary"] = "dynamodb",
        table_name: Optional[str] = os.environ.get("METADATA_TABLE", None),
        **data,
    ):
        super().__init__(**data)

        if db_type == "dynamodb":
            pass
        elif db_type == "temporary":
            pass
        else:
            raise Exception("Other database not yet supported")

    @classmethod
    def get_pynamodb_model(cls, table_name: Optional[str] = None):
        attributes: dict = {}

        for field_name, field_info in cls.model_fields.items():

            metadata = field_info.json_schema_extra["json_extra_schema"]
            if "__hash_key__" in metadata or "__range_key__" in metadata:
                if metadata.get("__hash_key__", False):
                    attributes[field_name] = UnicodeAttribute(hash_key=True)
                else:
                    attributes[field_name] = UnicodeAttribute(range_key=True)
            else:
                attributes[field_name] = PYDANTIC_PYNAMO_MAPPING.get(
                    field_info.annotation, UnicodeAttribute
                )(null=field_info.exclude)

        model_name = f"{cls.__name__}PynamoDBModel"
        PynamoDBBaseModel.Meta.table_name = table_name
        PynamoDBModel = type(model_name, (PynamoDBBaseModel,), attributes)

        cls.__PynamoDBModel__ = PynamoDBModel

        return PynamoDBModel

    def to_pynamodb_model(
        self, include: Optional[list | str] = "all", exclude: Optional[list] = []
    ) -> PynamoDBBaseModel:
        return self.__PynamoDBModel__(
            **self.model_serialize(
                include=include,
                exclude=exclude,
                serialization_alias=False,
            )
        )

    def model_serialize(
        self,
        include: Optional[list | str] = "all",
        exclude: Optional[list] = [],
        serialization_alias: Optional[bool] = True,
    ) -> dict[str, Any]:
        return self.model_dump(
            include=set(include) if type(include) == list else set(self.model_fields),
            exclude=set(exclude),
            by_alias=serialization_alias,
        )

    @classmethod
    def transform(
        cls, include: Optional[list | str] = "all", exclude: Optional[list] = []
    ) -> BaseModel:
        base_fields = {}

        for field_name, field_info in cls.model_fields.items():
            if include == "all":
                base_fields = {**cls.model_fields}
                break

            if field_name in include:
                base_fields[field_name] = field_info
            elif field_name in exclude:
                continue

        model_fields = {**BaseModel.model_fields, **base_fields}
        model_name = f"{cls.__name__}Custom"

        new_model: BaseModel = create_model(__model_name=model_name, __base__=cls)
        new_model.model_fields = model_fields

        return new_model
