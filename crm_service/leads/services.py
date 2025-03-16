from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from core.check_user_service import UserRoleService
from .dto_lead import LeadCreateDTO, LeadUpdateDTO
from .models import Lead

if TYPE_CHECKING:
    from ads.models import AdsCompany
    from django.contrib.auth.models import User


class LeadService(UserRoleService):
    """Сервис для работы с Лидами.

    Обеспечивает бизнес-логику создания и обновления лидов,
    включая проверку прав доступа и валидацию данных.
    """

    @classmethod
    def create_lead(cls, dto: LeadCreateDTO) -> Lead:
        """Создание лида."""
        cls._validate_lead_data(dto)
        cls._check_permissions_user(user=dto.created_by)

        with transaction.atomic():
            lead = Lead.objects.create(**dto.to_dict())
            lead.save()

        return lead

    @classmethod
    def update_lead(cls, dto: LeadUpdateDTO) -> Lead:
        """Обновление лида."""
        cls._validate_lead_data(dto)
        cls._check_permissions_user(user=dto.updated_by)

        with transaction.atomic():
            Lead.objects.filter(id=dto.id).update(**dto.to_dict())
            lead = Lead.objects.get(id=dto.id)
            lead.save()

        return lead

    @classmethod
    def _check_permissions_user(cls, user: "User") -> None:
        """Проверка перед созданием лида."""
        service_name = cls._get_service_name()
        cls._check_user_role(service_name=service_name, user=user)

    @classmethod
    def validate_name(cls, name: str, field_name: str) -> str:
        """Валидация имени, фамилии или отчества."""
        if len(name.split(" ")) > 1:
            raise ValidationError(
                _(f"{field_name} must consist of a single word or be separated '-'")
            )
        if len(name) < 2:
            raise ValidationError(
                _(f"{field_name} must contain at least 2 characters.")
            )
        return name

    @classmethod
    def validate_email(cls, email: str) -> str:
        """Валидация электронной почты."""
        if not email:
            raise ValidationError(_("Email is required."))
        return email

    @classmethod
    def validate_phone_number(cls, phone_number: str) -> str:
        """Валидация номера телефона."""
        if not phone_number:
            raise ValidationError(_("A phone number is required."))
        return phone_number

    @classmethod
    def validate_campaign(cls, campaign: "AdsCompany") -> "AdsCompany":
        """Валидация рекламной компании."""
        if not campaign:
            raise ValidationError(_("An advertising campaign is required."))
        return campaign

    @classmethod
    def _validate_lead_data(cls, dto: LeadCreateDTO | LeadUpdateDTO) -> None:
        """Валидация данных лида."""
        cls.validate_name(dto.first_name, "First Name")
        if dto.middle_name:
            cls.validate_name(dto.middle_name, "Middle Name")
        cls.validate_name(dto.last_name, "Last Name")
        cls.validate_email(dto.email)
        cls.validate_phone_number(dto.phone_number)
        cls.validate_campaign(dto.campaign)
