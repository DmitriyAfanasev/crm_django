from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models

from utils.mixins import TimestampMixin
from ads.models import AdsCompany


# TODO Оператор может создавать, просматривать и редактировать потенциальных клиентов.
class Lead(TimestampMixin, models.Model):
    """
    Модель перспективного клиента, но ещё не активного.
    Attributes:
        first_name (str): Имя
        middle_name (str): Отчество
        last_name (str): Фамилия
        phone_number (PhoneNumber): Номер телефона
        email (str): Электронная почта
        campaign (AdsCompany): Рекламная компания из которой он узнал об услуге.
    """

    first_name = models.CharField(
        max_length=100, blank=False, null=False, verbose_name=_("First Name")
    )
    middle_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Middle Name"), default=""
    )
    last_name = models.CharField(
        max_length=100, blank=False, null=False, verbose_name=_("Last Name")
    )
    phone_number = PhoneNumberField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("Phone Number"),
    )
    email = models.EmailField(
        unique=True, blank=False, null=False, verbose_name=_("Email")
    )
    campaign = models.ForeignKey(
        to=AdsCompany,
        on_delete=models.PROTECT,
        related_name="customers",
        verbose_name=_("Campaign"),
    )

    @property
    def full_name(self) -> str:
        """Возвращает полное имя клиента."""
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    @property
    def abbreviated_name(self) -> str:
        """
        Возвращает имя и отчество в виде инициалов с точкой не сокращая фамилию.
        Examples:
            Иван Сергеевич Иванов =>\n
            И. С. Иванов\n
            Иван Иванов =>\n
            И. Иванов
        """
        first_name = f"{self.first_name[0].capitalize()}."
        middle_name = f"{self.middle_name[0].capitalize()}." if self.middle_name else ""
        return f"{first_name} {middle_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} - {self.email}"
