from django.utils.translation import gettext_lazy as _

from django.db import models
from django.db.models import (
    CharField,
    DecimalField,
    ForeignKey,
    EmailField,
)

from service_product.models import Product
from utils.mixins import TimestampMixin
from utils.enums.countries import Country

from datetime import timedelta
from django.utils import timezone


class AdsCompany(TimestampMixin, models.Model):
    """
    Модель для рекламной компании

     Атрибуты:
        name (str): Название компании\n
        product (ForeignKey): Предоставляемая услуга\n
        channel (str): Каналы продвижения\n
        budget (int): Бюджет рекламной компании\n
        country (str): Страна в которой находится офис компании\n
        email (str): Электронная почта для обращений\n
        website (str): Вебсайт компании
    """

    class Meta:
        ordering: list[str] = ["name", "created_at"]
        verbose_name: str = _("Company")
        verbose_name_plural: str = _("Companies")
        unique_together: tuple[str,] = (("name", "website"),)

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
    channel: CharField = models.CharField(
        max_length=50,
        choices=[
            ("social_media", _("Social network")),
            ("search_engines", _("Search engines")),
            ("email", _("Email-newsletters")),
            ("contextual", _("Contextual advertising")),
            ("display", _("Display advertising")),
            ("offline", _("Offline channels")),
            ("partners", _("Partnership programs")),
            ("messengers", _("Messengers")),
            ("own_channels", _("Own channels")),
        ],
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
        return self.name

    def calculate_roi(self, revenue: float) -> float:
        """
        Рассчитывает ROI (Return on Investment) для рекламной компании.
        :param revenue: Доход, полученный от рекламной компании.
        :return: ROI в процентах.
        """
        if self.budget == 0:
            return 0.0
        return ((revenue - self.budget) / self.budget) * 100

    def get_full_website_url(self) -> str:
        """
        Возвращает полный URL вебсайта.
        """
        if self.website and not self.website.startswith(("http://", "https://")):
            return f"https://{self.website}"
        return self.website

    def is_active(self) -> bool:
        """
        Проверяет, активна ли рекламная компания.
        Компания считается активной, если она создана не более 30 дней назад.
        """
        return self.created_at >= timezone.now() - timedelta(days=30)
