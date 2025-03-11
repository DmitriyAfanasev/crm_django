from django.apps import apps
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from pydantic import EmailStr, Field

import requests
from requests import RequestException, Response

from ads.dto_ads_company import AdsCompanyCreateDTO
from ads.models import AdsCompany
from service_product.models import Product
from utils.mixins.services_mixins import BadWordsMixin
from core.check_user_service import UserRoleService


# TODO можно будет добавить рейтинг для заказчиков, и если у них хороший рейтинг, делать скидку или брать их заказы из очереди первыми.
class AdsCompanyService(BadWordsMixin, UserRoleService):
    name: str
    product: Product
    channel: str
    budget: float
    country: str
    email: EmailStr
    created_by: User
    website: str
    role: str = Field(default="marketer")

    @staticmethod
    def checking_before_creation(ads_company_dto: AdsCompanyCreateDTO) -> None:
        AdsCompanyService._check_existing_name_by_field_in_db(
            AdsCompany,
            ads_company_dto.name,
            _("A company with that name already exists."),
        )
        bad_words = AdsCompanyService._get_bad_words()

        AdsCompanyService._check_field_for_bad_words(
            field_name="name",
            text=ads_company_dto.name,
            bad_words=bad_words,
        )
        AdsCompanyService._check_field_for_bad_words(
            field_name="website",
            text=ads_company_dto.website,
            bad_words=bad_words,
        )
        AdsCompanyService._check_worked_website(ads_company_dto.website)

        user = User.objects.get(id=ads_company_dto.created_by)
        service_name = AdsCompanyService._get_service_name()
        AdsCompanyService._check_user_role(user=user, service_name=service_name)

    @staticmethod
    def _check_worked_website(website: str) -> bool:
        try:
            response: Response = requests.get(website, timeout=5)
            if response.status_code != 200:
                raise ValueError(_("The site is unavailable."))
            return True
        except RequestException as error:
            raise ValueError(_(f"The site is unavailable: {error}"))

    @staticmethod
    def get_leads_count(company) -> int:
        """Количество лидов компании"""
        return company.leads.count()

    @staticmethod
    def get_customers_count(company) -> int:
        """Количество конвертированных клиентов"""
        return company.leads.filter(customer__isnull=False).count()

    @staticmethod
    def calculate_profit(company) -> float:
        """Расчет процентной прибыли компании."""
        Contract = apps.get_model("contracts.Contract")

        total_income = (
            Contract.objects.filter(customer__lead__campaign=company).aggregate(
                income=Sum("cost")
            )["income"]
            or 0
        )  # Защита от None

        if company.budget == 0:
            return 0.0

        profit_percentage = ((total_income - company.budget) / company.budget) * 100
        return round(profit_percentage, 2)
