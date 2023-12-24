import uuid
from typing import Optional

import pydantic


class UserResponseBase(pydantic.BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True  # Set from_attributes to True


class UserResponse(UserResponseBase):
    id: uuid.UUID
    username: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    email: Optional[str]


class UserCreateResponse(UserResponse):
    token: Optional[str] = None


class UserLoginResponse(UserResponseBase):
    id: uuid.UUID
    token: Optional[str] = None
