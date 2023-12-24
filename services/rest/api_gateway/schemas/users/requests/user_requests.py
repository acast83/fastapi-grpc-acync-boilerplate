from typing import Optional

import pydantic


class UserRequestSchema(pydantic.BaseModel):
    pass


class UserCreateRequest(UserRequestSchema):
    username: str
    first_name: str
    last_name: str
    password: str
    email: Optional[str]


class UserLoginRequest(UserRequestSchema):
    username: str
    password: str
