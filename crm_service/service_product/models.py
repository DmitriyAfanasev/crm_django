from django.utils.translation import gettext_lazy as _

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from mixins import TimestampMixin


class Product(TimestampMixin, models.Model):
    """Модель услуги для клиентов."""

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        db_index=True,
        verbose_name=_("Service name"),
    )
    description = models.TextField(
        blank=False,
        null=False,
        verbose_name=_("Service description"),
    )
    cost = models.FloatField(
        validators=[MinValueValidator(0.0)],
        blank=False,
        null=False,
        verbose_name=_("Service cost"),
    )
    discount = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        blank=False,
        null=False,
        verbose_name=_("Discount percentage"),
    )
    status = models.CharField(
        max_length=20,
        default="inactive",
        blank=False,
        null=False,
        verbose_name=_("Service status"),
        choices=[
            ("active", _("Active")),
            ("inactive", _("Inactive")),
            ("in_development", _("In-Development")),
        ],
    )
    archived = models.BooleanField(default=False, verbose_name=_("Archived"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ("name", "created_at")
        db_table = "service_products"

    def __str__(self) -> str:
        return self.name

    @property
    def final_cost(self) -> float:
        """Рассчитывает итоговую стоимость с учётом скидки."""
        return self.cost * (1 - self.discount / 100)
