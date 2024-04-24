from typing import Pattern

from base_model import BaseModel, field


class UserModel(BaseModel):
    username: str = field(alias="username", min_length=1, is_hash_key=True)
    email: str = field(alias="email", min_length=1, is_range_key=True)
    datetime: str = field(
        alias="datetime", pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    )
    test_frozen: str = field(default="", alias="test_frozen", frozen=True)


user_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "datetime": "2012-12-01 02:01:02",
}
pydantic_user = UserModel(database="rds", table_name="test", **user_data)
pynamo_db_model = pydantic_user.get_pynamodb_model()

print(pynamo_db_model.serialize())
print(pydantic_user.model_dump())

pydantic_user.test_frozen = "new"
