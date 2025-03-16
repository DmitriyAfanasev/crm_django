from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .base import BaseService


class UserRoleService(BaseService):
    """
    Сервис для проверки ролей пользователей.

    Атрибуты:
        roles (dict): Словарь, связывающий сервисы с требуемыми ролями.
    """

    roles = {
        "AdsCompanyService": "marketer",
        "ProductService": "marketer",
        "LeadService": "operator",
        "ContractService": "manager",
        "CustomerService": "manager",
    }

    @classmethod
    def _check_user_role(cls, user: User, service_name: str) -> None:
        """
        Проверяет, имеет ли пользователь одну из требуемых ролей,
        или является он администратором сервиса.
        """
        required_role = cls.roles.get(service_name)
        if required_role is None:
            raise ValueError(_("No role defined for this service."))

        if (
            not user.groups.filter(name=required_role).exists()
            and not user.is_superuser
        ):
            raise ValueError(
                _(
                    f"The user must be a member of the '{required_role}' group or an admin."
                )
            )
