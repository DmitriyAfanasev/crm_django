from typing import TYPE_CHECKING

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

import requests
from requests import Response

from ads.dto_ads_company import AdsCompanyCreateDTO, AdsCompanyUpdateDTO
from ads.models import AdsCompany

from utils.mixins.services_mixins import BadWordsMixin
from core.check_user_service import UserRoleService

if TYPE_CHECKING:
    from contracts.models import Contract


class AdsCompanyService(BadWordsMixin, UserRoleService):
    """Сервис для работы с рекламными компаниями.

    Обеспечивает бизнес-логику создания и обновления компаний,
    включая проверку прав доступа и валидацию данных.
    """

    @classmethod
    def create_company(cls, dto: AdsCompanyCreateDTO) -> AdsCompany:
        """Создает рекламную компанию."""
        cls._checking_before_creation(dto)

        with transaction.atomic():
            company = AdsCompany.objects.create(**dto.to_dict())
            company.save()
        return company

    @classmethod
    def update_company(cls, dto: AdsCompanyUpdateDTO) -> AdsCompany:
        """Обновляет рекламную компанию."""
        cls._checking_before_update(dto)

        with transaction.atomic():
            AdsCompany.objects.filter(id=dto.id).update(**dto.to_dict())
            company = AdsCompany.objects.get(id=dto.id)
            company.save()

        return company

    @staticmethod
    def validate_name(name: str) -> None:
        """Проверяет, что имя рекламной компании не короче 3 символов."""
        if len(name) < 3:
            raise ValidationError(_("Name must be at least 3 characters long."))

    @staticmethod
    def validate_budget(budget: float, product_cost: float) -> None:
        """Проверяет, что бюджет не меньше стоимости услуги."""
        if budget < product_cost:
            raise ValidationError(_("The budget cannot be less than the product cost."))

    @staticmethod
    def validate_country(country: str) -> None:
        """Проверяет, что страна указана."""
        if not country:
            raise ValidationError(_("Country must be provided."))

    @staticmethod
    def validate_website(website: str) -> str:
        """Проверяет, что веб-сайт начинается с HTTPS."""
        if not website:
            raise ValidationError(_("Website must be provided."))
        if website.startswith("http://"):
            raise ValidationError(_("Website must be secure (use HTTPS)."))
        return website if website.startswith("https://") else f"https://{website}"

    @classmethod
    def _validate_common_fields(
        cls, dto: AdsCompanyCreateDTO | AdsCompanyUpdateDTO
    ) -> None:
        """Проверяет общие поля для создания и обновления компании."""
        cls.validate_name(dto.name)
        cls.validate_budget(dto.budget, dto.product.cost)
        cls.validate_country(dto.country)
        cls.validate_website(dto.website)

    @classmethod
    def _checking_before_creation(cls, dto: AdsCompanyCreateDTO) -> None:
        """Проверяет данные перед созданием рекламной компании."""
        cls._validate_common_fields(dto)
        cls._check_existing_name(dto.name)
        cls._check_for_bad_words(dto)
        cls._check_worked_website(dto.website)
        cls._check_permissions_user(dto.created_by)

    @classmethod
    def _checking_before_update(cls, dto: AdsCompanyUpdateDTO) -> None:
        """Проверяет данные перед обновлением рекламной компании."""
        cls._validate_common_fields(dto)
        cls._check_for_bad_words(dto)
        cls._check_worked_website(dto.website)

    @classmethod
    def _check_existing_name(cls, name: str) -> None:
        """Проверяет, что имя компании уникально."""
        cls._check_existing_name_by_field_in_db(
            AdsCompany,
            name,
            _("A company with that name already exists."),
        )

    @classmethod
    def _check_for_bad_words(
        cls, dto: AdsCompanyCreateDTO | AdsCompanyUpdateDTO
    ) -> None:
        """Проверяет наличие запрещенных слов в имени и веб-сайте."""
        bad_words = cls._get_bad_words()
        cls._check_field_for_bad_words("name", dto.name, bad_words)
        cls._check_field_for_bad_words("website", dto.website, bad_words)

    @classmethod
    def _check_permissions_user(cls, user) -> None:
        """Проверяет роль пользователя."""
        service_name = cls._get_service_name()
        cls._check_user_role(user=user, service_name=service_name)

    @staticmethod
    def _check_worked_website(website: str) -> bool:
        """Проверяет доступность вебсайта."""
        try:
            response: Response = requests.get(website, timeout=5)
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            raise ValidationError(_(f"The site returned an error: {e}")) from e
        except requests.exceptions.RequestException as e:
            raise ValidationError(_(f"The site is unavailable: {e}")) from e

    @staticmethod
    def get_leads_count(company: AdsCompany) -> int:
        """Подсчитывает и возвращает количество лидов компании."""
        return company.leads.count()

    @staticmethod
    def get_customers_count(company: AdsCompany) -> int:
        """Подсчитывает и возвращает количество активных клиентов."""
        return company.leads.filter(customer__isnull=False).count()

    @classmethod
    def calculate_profit(cls, company: AdsCompany) -> float:
        """Расчет прибыли компании."""
        total_income = cls.total_income(company)
        profit: float = total_income - company.budget
        return round(profit, 2)

    @classmethod
    def calculate_roi(cls, company: AdsCompany) -> float:
        """Расчет ROI (соотношение доходов к затратам)."""
        total_income = cls.total_income(company)
        if company.budget == 0:
            return 0.0
        roi: float = total_income / company.budget
        return round(roi, 2)

    @classmethod
    def total_income(cls, company: AdsCompany) -> float:
        """Возвращает общий доход компании."""
        contract: type["Contract"] = apps.get_model("contracts", "Contract")
        return (
            contract.objects.filter(customer__lead__campaign=company).aggregate(
                income=Sum("cost")
            )["income"]
            or 0
        )
