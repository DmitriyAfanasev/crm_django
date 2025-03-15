from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass
from django.contrib.auth.models import User
from core.base import BaseDTO

if TYPE_CHECKING:
    from service_product.models import Product


@dataclass
class AdsCompanyDTO(BaseDTO):
    """
    Data Transfer Object (DTO) для представления рекламной компании.

    Атрибуты:
        id (Optional[int]): Уникальный идентификатор рекламной компании. Может быть None для новых компаний.
        name (str): Название рекламной компании.
        product (Product): Продукт, связанный с рекламной компанией.
        channel (str): Канал, через который осуществляется реклама.
        budget (float): Бюджет рекламной компании.
        country (str): Страна, в которой проводится реклама.
        email (str): Электронная почта для связи.
        website (str): Веб-сайт рекламной компании.
        created_by (Optional[User]): Пользователь, создавший рекламную компанию. Может быть None.
        updated_by (Optional[User]): Пользователь, обновивший рекламную компанию. Может быть None.
    """

    name: str
    product: "Product"
    channel: str
    budget: float
    country: str
    email: str
    website: str
    created_by: Optional[User] = None
    updated_by: Optional[User] = None
    id: Optional[int] = None


@dataclass
class AdsCompanyCreateDTO(AdsCompanyDTO):
    """
    Data Transfer Object (DTO) для создания рекламной компании.

    Наследует все атрибуты AdsCompanyDTO, но требует указания created_by.

    Атрибуты:
        created_by (User): Пользователь, создавший рекламную компанию.
    """

    created_by: User


@dataclass
class AdsCompanyUpdateDTO(AdsCompanyDTO):
    """
    Data Transfer Object (DTO) для обновления рекламной компании.

    Наследует все атрибуты AdsCompanyDTO, но требует указания id и updated_by.

    Атрибуты:
        id (int): Уникальный идентификатор рекламной компании.
        updated_by (User): Пользователь, обновивший рекламную компанию.
    """

    id: int
    updated_by: User
