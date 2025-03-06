from typing import Optional, TYPE_CHECKING
from django.contrib.auth.models import User
from core.base import BaseDTO

if TYPE_CHECKING:
    from leads.models import Lead


class DTOCustomers(BaseDTO):
    """
    Data Transfer Object (DTO) для представления информации о клиенте.

    Атрибуты:
        pk (Optional[int]): Уникальный идентификатор клиента. Может быть None для новых клиентов.
        lead (Lead): Лид, которым является клиент.
        is_active (bool): Статус активности клиента.
        created_by (Optional[User]): Пользователь, создавший запись о клиенте. Может быть None.
        updated_by (Optional[User]): Пользователь, обновивший запись о клиенте. Может быть None.
    """

    pk: Optional[int]
    lead: "Lead"
    is_active: bool
    created_by: Optional[User]
    updated_by: Optional[User]


class DTOCustomersCreate(DTOCustomers):
    """
    Data Transfer Object (DTO) для создания клиента.

    Наследует все атрибуты DTOCustomers, но требует указания created_by.

    Атрибуты:
        created_by (User): Пользователь, создавший запись о клиенте.
    """

    created_by: User


class DTOCustomersUpdate(DTOCustomers):
    """
    Data Transfer Object (DTO) для обновления клиента.

    Наследует все атрибуты DTOCustomers, но требует указания pk и updated_by.

    Атрибуты:
        pk (int): Уникальный идентификатор клиента.
        updated_by (User): Пользователь, обновивший запись о клиенте.
    """

    pk: int
    updated_by: User
