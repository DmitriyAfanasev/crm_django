from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from utils.mixins import TimestampMixin, ActorMixin
from ads.models import AdsCompany


class Lead(TimestampMixin, ActorMixin):
    """
    Модель перспективного клиента, но ещё не активного.

    Attributes:
        first_name (str): Имя.
        middle_name (str): Отчество.
        last_name (str): Фамилия.
        phone_number (PhoneNumber): Номер телефона.
        email (str): Электронная почта.
        campaign (AdsCompany): Рекламная компания, из которой он узнал об услуге.
        is_active (bool): Статус активности лида.
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
        related_name="leads",
        verbose_name=_("Campaign"),
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("Is Active"),
    )

    @property
    def name(self) -> str:
        """Возвращает адрес электронной почты лида."""
        # чтобы при удалении лида, в сообщение было понятно, какой объект был удалён

        return self.email

    @property
    def full_name(self) -> str:
        """Возвращает полное имя клиента."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    @property
    def abbreviated_name(self) -> str:
        """
        Возвращает имя и отчество в виде инициалов с точкой, не сокращая фамилию.

        Примеры:
            Иван Сергеевич Иванов => И. С. Иванов
            Иван Иванов => И. Иванов
        """
        first_name_initial = f"{self.first_name[0].capitalize()}."
        middle_name_initial = (
            f"{self.middle_name[0].capitalize()}." if self.middle_name else ""
        )
        return f"{first_name_initial} {middle_name_initial} {self.last_name}".strip()

    def __str__(self) -> str:
        """Возвращает полное имя лида."""
        return self.full_name
