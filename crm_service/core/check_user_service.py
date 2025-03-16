from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .base import BaseService


class UserActiveService(BaseService):
    """Проверяет, является ли пользователь активным."""

    @staticmethod
    def _check_active_user(user_id: int) -> None:
        if not User.objects.filter(id=user_id, is_active=True).exists():
            raise ValueError(_("The creator must be an active user."))


class UserRoleService(UserActiveService):
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

    @staticmethod
    def _check_user_role(user: User, service_name: str) -> None:
        """
        Проверяет, имеет ли пользователь одну из требуемых ролей,
        или является он администратором сервиса.
        """
        required_role = UserRoleService.roles.get(service_name)
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
