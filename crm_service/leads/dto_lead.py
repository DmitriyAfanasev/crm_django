from dataclasses import dataclass

from typing import Optional, TYPE_CHECKING

from core.base import BaseDTO

if TYPE_CHECKING:
    from ads.models import AdsCompany
    from django.contrib.auth.models import User


@dataclass
class BaseLeadDTO(BaseDTO):
    """
    Data Transfer Object (DTO) для представления базовой информации о лиде.

    Attributes:
        pk (Optional[int]): Уникальный идентификатор лида. Может быть None для новых лидов.
        first_name (str): Имя лида.
        middle_name (Optional[str]): Отчество лида. Может быть None.
        last_name (str): Фамилия лида.
        email (str): Электронная почта лида.
        phone_number (str): Номер телефона лида.
        campaign ("AdsCompany"): Рекламная компания, связанная с лидом.
        created_by (Optional[User]): Пользователь, создавший лид. Может быть None.
        updated_by (Optional[User]): Пользователь, обновивший лида. Может быть None.
    """

    first_name: str
    last_name: str
    email: str
    phone_number: str
    campaign: "AdsCompany"
    pk: Optional[int] = None
    middle_name: Optional[str] = None
    created_by: Optional[User] = None
    updated_by: Optional[User] = None


@dataclass
class LeadCreateDTO(BaseLeadDTO):
    """
    Data Transfer Object (DTO) для создания лида.

    Наследует все атрибуты BaseLeadDTO, но требует указания created_by.

    Attributes:
        created_by (User): Пользователь, создавший лид.
    """

    created_by: User


@dataclass
class LeadUpdateDTO(BaseLeadDTO):
    """
    Data Transfer Object (DTO) для обновления лида.

    Наследует все атрибуты LeadCreateDTO, но требует указания pk и updated_by.

    Attributes:
        pk (int): Уникальный идентификатор лида.
        updated_by (User): Пользователь, обновивший лид.
    """

    pk: int
    updated_by: User
