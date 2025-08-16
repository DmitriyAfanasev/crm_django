from django.contrib.auth import get_user_model
from ninja.schema import Schema
from pydantic import EmailStr


User = get_user_model()


class UserSchema(Schema):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
