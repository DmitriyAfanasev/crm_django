import datetime
from decimal import Decimal

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.files import File
from django.contrib.auth.models import User
from django.db import transaction, DatabaseError

from .models import Contract
from core.check_user_service import UserRoleService
from .dto_contracts import ContractCreateDTO, ContractUpdateDTO

import logging

logger = logging.getLogger(__name__)


class ContractService(UserRoleService):
    """Сервис для работы с контрактами.

    Обеспечивает бизнес-логику создания и обновления контрактов,
    включая проверку прав доступа и валидацию данных.
    """

    @classmethod
    def create_contract(cls, dto: ContractCreateDTO) -> Contract:
        """Создание контракта"""
        cls._checking_before_creation(dto)
        with transaction.atomic():
            contract: Contract = Contract.objects.create(**dto.to_dict())
            contract.save()

        return contract

    @classmethod
    def update_contract(cls, dto: ContractUpdateDTO) -> Contract:
        """Обновление данных в контракте."""
        service_name: str = cls._get_service_name()
        user: User = dto.updated_by
        cls._check_user_role(user, service_name)
        cls.validate_dates(dto.start_date, dto.end_date)
        cls.validate_file(dto.file_document)

        try:
            with transaction.atomic():
                Contract.objects.filter(id=dto.id).update(**dto.to_dict())
                contract = Contract.objects.get(id=dto.id)
                contract.save()
                contract.refresh_from_db()
        except DatabaseError as error:
            logger.error(f"Database error occurred: {error}")
            raise ValidationError(_("An error occurred while updating the contract."))

        return contract

    @classmethod
    def _checking_before_creation(cls, dto: ContractCreateDTO) -> None:
        """Проверка прав пользователя перед созданием контракта."""
        service_name: str = cls._get_service_name()
        user: User = dto.created_by
        cls._check_user_role(user, service_name)

    @classmethod
    def _date_matching_check(cls, start: datetime, end: datetime) -> None:
        """Проверяет корректность временного интервала."""
        if start > end:
            raise ValidationError(_("Start date must be greater than end date"))

    @classmethod
    def _validate_start_date(cls, start: datetime) -> None:
        if start < datetime.date.today():
            raise ValidationError(_("Start date must be greater than today"))

    @classmethod
    def validate_dates(cls, start_date: datetime.date, end_date: datetime.date) -> None:
        """Проверяет корректность дат контракта."""
        cls._date_matching_check(start_date, end_date)
        cls._validate_start_date(start_date)

        min_duration = datetime.timedelta(days=1)
        if (end_date - start_date) < min_duration:
            raise ValidationError(_("The contract duration must be at least 1 day."))

        max_duration = datetime.timedelta(days=365 * 5)
        if (end_date - start_date) > max_duration:
            raise ValidationError(_("The contract duration cannot exceed 5 years."))

    @classmethod
    def validate_file(cls, file_document: File) -> None:
        """Проверяет корректность файла контракта."""
        allowed_extensions = {".pdf", ".docx"}
        if not any(
            file_document.name.lower().endswith(ext) for ext in allowed_extensions
        ):
            raise ValidationError(_("Only PDF and DOCX files are allowed."))

        max_size = 10 * 1024 * 1024  # 10 МБ
        if file_document.size > max_size:
            raise ValidationError(
                _("The file size cannot exceed {} MB. Your file size: {} MB").format(
                    max_size // (1024 * 1024), file_document.size // (1024 * 1024)
                )
            )

    @classmethod
    def validate_cost(
        cls, cost_data: float, contract_pk: int = None, user: User = None
    ) -> None:
        """
        Проверяет стоимость контракта согласно бизнес-правилам.

        Бизнес-правила:
            1. Стоимость должна быть положительной
            2. Запрещено снижение стоимости более чем на 30%
               от исходного значения (если пользователь не superuser)
            3. Запрещено любое снижение стоимости для обычных пользователей
        """
        if cost_data <= 0:
            raise ValidationError(_("The cost is invalid."))

        if contract_pk is None:
            return

        contract: Contract = Contract.objects.get(pk=contract_pk)
        current_cost: Decimal = Decimal(contract.cost)
        min_allowed_cost: Decimal = current_cost * Decimal("0.7")

        is_over_30_percent: bool = Decimal(cost_data) < min_allowed_cost

        if contract.cost:
            if not user.is_superuser and is_over_30_percent:
                raise ValidationError(
                    _("Cost reduction exceeds 30% limit. ")
                    + _("Current value: %(current)s. Minimum allowed: %(min)s")
                    % {"current": contract.cost, "min": min_allowed_cost},
                )
