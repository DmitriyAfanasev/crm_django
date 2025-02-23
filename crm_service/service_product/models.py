from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import (
    CharField,
    TextField,
    PositiveSmallIntegerField,
    FloatField,
    BooleanField,
)
from django.core.validators import MinValueValidator, MaxValueValidator

from mixins import TimestampMixin


class Product(TimestampMixin, models.Model):
    """
    Модель услуги для клиентов.

    Атрибуты:
        name (str): Название услуги
        description (str): Описание услуги
        cost (float): Стоимость услуги
        discount (int): Процент скидки на услугу (от 0 до 50)
        status (str): Статус услуги (активна, неактивна, в разработке)
        archived (bool): Флаг, указывающий, архивирована ли услуга
    """

    name: CharField = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        db_index=True,
        verbose_name=_("Service name"),
    )
    description: TextField = models.TextField(
        blank=False,
        null=False,
        verbose_name=_("Service description"),
    )
    cost: FloatField = models.FloatField(
        validators=[MinValueValidator(0.0)],
        blank=False,
        null=False,
        verbose_name=_("Service cost"),
    )
    discount: PositiveSmallIntegerField = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        blank=False,
        null=False,
        verbose_name=_("Discount percentage"),
    )
    status: CharField = models.CharField(
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
    archived: BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("Archived"),
    )

    class Meta:
        """
        Метаданные модели.

        Атрибуты:
            verbose_name (str): Имя модели в единственном числе
            verbose_name_plural (str): Имя модели во множественном числе
            ordering (tuple): Порядок сортировки по умолчанию
            db_table (str): Имя таблицы в базе данных
        """

        verbose_name: str = _("Product")
        verbose_name_plural: str = _("Products")
        ordering: tuple[str, str] = ("name", "created_at")
        db_table: str = "service_products"

    def __str__(self) -> str:
        """Возвращает строковое представление объекта, а точнее название услуги."""
        return self.name

    @property
    def final_cost(self) -> float:
        """
        Рассчитывает итоговую стоимость услуги с учётом скидки.

        Возвращает:
            float: Итоговая стоимость услуги.
        """
        return self.cost * (1 - self.discount / 100)
