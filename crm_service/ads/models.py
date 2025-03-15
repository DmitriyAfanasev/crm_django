from functools import cached_property
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import (
    CharField,
    DecimalField,
    ForeignKey,
    EmailField,
)

from service_product.models import Product
from utils.mixins import TimestampMixin, ActorMixin
from utils.enums import Country
from .models_as_description import PromotionChannel

if TYPE_CHECKING:
    from .services import AdsCompanyService


class AdsCompany(TimestampMixin, ActorMixin):
    """
    Модель для рекламной компании.

    Атрибуты:
        name (str): Название компании.
        product (ForeignKey): Предоставляемая услуга.
        channel (ForeignKey): Каналы продвижения.
        budget (Decimal): Бюджет рекламной компании.
        country (str): Страна, в которой находится офис компании.
        email (str): Электронная почта для обращений.
        website (str): Вебсайт компании.
    """

    class Meta:
        ordering: list[str] = ["name", "created_at"]
        verbose_name: str = _("Company")
        verbose_name_plural: str = _("Companies")
        unique_together: tuple[str, ...] = (("name", "website"),)

    name: CharField = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        db_index=True,
        verbose_name=_("Company name"),
    )
    product: ForeignKey = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name="service"
    )
    channel: ForeignKey = models.ForeignKey(
        to=PromotionChannel,
        on_delete=models.PROTECT,
        verbose_name=_("Promotion channel"),
    )
    budget: DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name=_("Budget"),
    )
    country: CharField = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Country"),
        choices=Country.choices(),
    )
    email: EmailField = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("Email address"),
    )
    website: CharField = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name=_("Website"),
        help_text=_("Link to the website company"),
    )

    def __str__(self) -> str:
        """Возвращает название рекламной компании."""
        return self.name

    @cached_property
    def _service(self) -> "AdsCompanyService":
        """Возвращает экземпляр сервиса для работы с рекламной компанией."""
        from .services import AdsCompanyService

        return AdsCompanyService()

    @property
    def leads_count(self) -> int:
        """Возвращает количество лидов рекламной компании."""
        return self._service.get_leads_count(self)

    @property
    def customers_count(self) -> int:
        """Возвращает количество активных клиентов рекламной компании."""
        return self._service.get_customers_count(self)

    @property
    def profit(self) -> float:
        """Возвращает прибыль для данной рекламной компании."""
        return self._service.calculate_profit(self)

    @property
    def roi(self) -> float:
        """Возвращает соотношение доходов к затратам."""
        return self._service.calculate_roi(self)
