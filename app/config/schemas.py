from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from . import models


class BaseUser(BaseModel):
    firstname: str | None = Field(default=..., example="Martín", min_length=3, max_length=100)
    lastname: str | None = Field(default=..., example="Zayas", min_length=3, max_length=100)
    email: EmailStr | None = Field(default=..., example="mail@example.com")

class UserIn(BaseUser):
    password: str | None = Field(default=..., example="password", min_length=8, max_length=100)
    role_id: int | None = Field(default=...)

class UserUpdate(BaseUser):
    firstname: str | None = Field(default=None, example="Martín", min_length=3, max_length=100)
    lastname: str | None = Field(default=None, example="Zayas", min_length=3, max_length=100)
    email: EmailStr | None = Field(default=None, example="mail@example.com")
    password: str | None = Field(default=None, example="password", min_length=8, max_length=100)
    active: bool | None

class UserOut(BaseUser):
    id: int
    active: bool | None
    role_id: int | None
    created_by: int | None
    updated_by: int | None
    created_at: datetime
    updated_at: datetime

class Role():
    id: int | None = Field(default=None)
    name: str | None = Field(default=None)
    