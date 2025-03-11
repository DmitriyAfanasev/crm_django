from django.contrib.auth.models import User
from core.base import BaseDTO
from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseProductDTO(BaseDTO):
    """
    Data Transfer Object (DTO) для представления базовой информации об услуге.

    Attributes:
        pk (Optional[int]): id услуги. Может быть None, если ещё не создана.
        name (str): Название.
        description (str): Описание.
        cost (float): Стоимость.
        discount (int): Скидка на услугу в процентах.
        status (str): Доступна она или возможно в разработке.
        archived (bool): Архивирована ли услуга.
        created_by (Optional[User]): id, создавшего услугу. Может быть None.
        updated_by (Optional[User]): id, обновившего данные. Может быть None.
    """

    name: str
    description: str
    cost: float
    discount: int
    status: str
    archived: bool
    pk: Optional[int] = None
    created_by: Optional[User] = None
    updated_by: Optional[User] = None


@dataclass
class ProductCreateDTO(BaseProductDTO):
    """
    Data Transfer Object (DTO) для создания продукта.

    Наследует все атрибуты BaseProductDTO, но требует указания created_by.
    """

    created_by: User


@dataclass
class ProductUpdateDTO(BaseProductDTO):
    """
    Data Transfer Object (DTO) для обновления продукта.

    Наследует все атрибуты ProductCreateDTO, но требует указания pk и updated_by.
    """

    pk: int
    updated_by: User
