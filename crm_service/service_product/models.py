from django.utils.translation import gettext_lazy as _

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from mixins import TimestampMixin


class Product(TimestampMixin, models.Model):
    """Модель услуги для клиентов."""

    name = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    description = models.TextField(blank=False, null=False)
    cost = models.FloatField(
        validators=[MinValueValidator(0.0)], blank=False, null=False
    )
    discount = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("active", _("Active")),
            ("inactive", _("Inactive")),
        ],
        default="inactive",
    )

    def __str__(self):
        return self.name, self.status

    @property
    def final_cost(self):
        """Рассчитывает итоговую стоимость с учётом скидки."""
        return self.cost * (1 - self.discount / 100)
