from base_model import BaseModel, field


class UserModel(BaseModel):
    username: str = field(alias="username", min_length=1, is_hash_key=True)
    email: str = field(alias="email", min_length=1, is_range_key=True)


user_data = {"username": "john_doe", "email": "john@example.com"}
pydantic_user = UserModel(database="rds", table_name="test", **user_data)
pynamo_db_model = pydantic_user.get_pynamodb_model()

print(pynamo_db_model.serialize())
print(pydantic_user.model_dump())
