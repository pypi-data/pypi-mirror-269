from base_model import BaseModel, field


class UserModel(BaseModel):
    username: str = field(min_length=1, is_hash_key=True)
    email: str = field(min_length=1, is_range_key=True)
    datetime: str = field(pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
    test_frozen: str = field(default="", alias="test_frozen", frozen=True)
    new_field: str = field(validation_alias="check", serialization_alias="serial")
    updated_by: str = field(exclude=True)


class TestExclude(BaseModel):
    test_exclude: str


class TestMetaData(BaseModel): ...


user_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "datetime": "2012-12-01 02:01:02",
    "check": "1",
    "created_by": "a",
    "updated_by": "a",
    "non_defined": "test",
}
test_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "datetime": "2012-12-01 02:01:02",
    "check": "1",
    "updated_by": "a",
    "non_defined": "test",
}

tmdata = TestMetaData(**test_data)
print(tmdata)
# print(tmdata.created_by)
test_model = TestExclude.transform(exclude=["test_exclude"])
print(test_model.model_fields.keys())
test = test_model(**user_data)
print(test)
print(test.database_model)
temp_model = UserModel.transform(include=["username"])
temp = temp_model(db_type="dynamodb", table_name="test", **user_data)
print(temp)
print(temp.database_model.get_attributes())
pydantic_user = UserModel(db_type="dynamodb", table_name="test", **user_data)
print(pydantic_user)
print(pydantic_user.database_model.get_attributes())
pynamo_db_model = pydantic_user.to_pynamodb_model()
print(pynamo_db_model.serialize())
print(pydantic_user.model_serialize())
print(temp.model_serialize())

pydantic_user.test_frozen = "new"
