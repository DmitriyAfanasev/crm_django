from django.contrib.auth.models import User

from dataclasses import dataclass
from typing import Optional

from ads.models import AdsCompany

from core.base import BaseDTO


@dataclass
class BaseLeadDTO(BaseDTO):
    """Базовый DTO класс Лида."""

    pk: Optional[int]
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: str
    phone_number: str
    campaign: AdsCompany
    created_by: User
    updated_by: Optional[User]


@dataclass
class LeadCreateDTO(BaseLeadDTO):
    """DTO класс без поля pk, так как лид ещё не создан."""

    created_by: User


@dataclass
class LeadUpdateDTO(LeadCreateDTO):
    """Класс для передачи лида с обновлёнными данными, updated_by становится обязательным."""

    pk: int
    updated_by: User
