from datetime import datetime
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from django.contrib.auth.models import User
from django.core.files.base import File

from core.base import BaseDTO

if TYPE_CHECKING:
    from service_product.models import Product


@dataclass
class ContractDTO(BaseDTO):
    """
    Data Transfer Object (DTO) для представления контракта.

    Attributes:
        id (Optional[int]): Уникальный идентификатор контракта. Может быть None у новых контрактов.
        name (str): Название контракта.
        product (Product): Продукт, связанный с контрактом.
        file_document (File): Файл документа контракта.
        start_date (datetime): Дата начала контракта.
        end_date (datetime): Дата окончания контракта.
        cost (float): Стоимость контракта.
        created_by (Optional[User]): Пользователь, создавший контракт. Может быть None.
        updated_by (Optional[User]): Пользователь, обновивший контракт. Может быть None.
    """

    name: str
    product: "Product"
    file_document: File
    start_date: datetime
    end_date: datetime
    cost: float
    id: Optional[int] = None
    created_by: Optional[User] = None
    updated_by: Optional[User] = None


@dataclass
class ContractCreateDTO(ContractDTO):
    """
    Data Transfer Object (DTO) для создания контракта.

    Наследует все атрибуты ContractDTO, но требует указания created_by.

    Attributes:

        created_by (User): Пользователь, создавший контракт.
    """

    created_by: User


@dataclass
class ContractUpdateDTO(ContractDTO):
    """
    Data Transfer Object (DTO) для обновления контракта.

    Наследует все атрибуты ContractDTO, но требует указания pk и updated_by.

    Attributes:
        id (int): Уникальный идентификатор контракта.
        updated_by (User): Пользователь, обновивший контракт.
    """

    id: int
    updated_by: User
