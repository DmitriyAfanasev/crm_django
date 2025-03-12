from django.db.models import CharField, OneToOneField, FileField
from django.db.models.fields import DateField, DecimalField
from django.utils.translation import gettext_lazy as _
from django.db import models

from service_product.models import Product
from utils.mixins import TimestampMixin, ActorMixin


def create_directory_path_for_documents_customer(
    instance: "Contract", filename: str
) -> str:
    """Создаётся путь к каталогу, в котором будут храниться документы."""
    return "documents/{agreement}-{date}/{filename}".format(
        agreement=instance.name, date=instance.start_date, filename=filename
    )


class Contract(TimestampMixin, ActorMixin):
    """
    Модель для представления контракта.

    Атрибуты:
        name (CharField): Название контракта.
        product (OneToOneField): Услуга, связанная с контрактом.
        file_document (FileField): Файл с документами.
        start_date (DateField): Дата начала контракта.
        end_date (DateField): Дата окончания контракта.
        cost (DecimalField): Стоимость контракта.
    """

    name: CharField = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_("Contract Name"),
        db_index=True,
    )
    product: OneToOneField = models.OneToOneField(
        to=Product,
        on_delete=models.PROTECT,
        verbose_name=_("Service"),
    )
    file_document: FileField = models.FileField(
        blank=False,
        null=False,
        upload_to=create_directory_path_for_documents_customer,
        verbose_name=_("File with documents"),
    )
    start_date: DateField = models.DateField(
        blank=False,
        null=False,
        verbose_name=_("Start date"),
    )
    end_date: DateField = models.DateField(
        blank=False,
        null=False,
        verbose_name=_("End date"),
    )
    cost: DecimalField = models.DecimalField(
        blank=False, null=False, max_digits=15, decimal_places=2, verbose_name=_("Cost")
    )

    def __str__(self) -> str:
        """Возвращает название контракта."""
        return self.name
