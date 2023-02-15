from pydantic import BaseModel, EmailStr
from datetime import datetime


class BaseUser(BaseModel):
    firstname: str | None
    lastname: str | None
    email: EmailStr | None

class UserIn(BaseUser):
    password: str | None

class UserOut(BaseUser):
    id: int
    active: bool | None
    created_by: int | None
    updated_by: int | None
    created_at: datetime
    updated_at: datetime