from django.utils.translation import gettext_lazy as _

from django.db import models

from service_product.models import Product


def create_directory_path_for_documents_customer(
    instance: "Customer", filename: str
) -> str:
    """Создаётся путь к каталогу, в котором будут храниться документы."""
    return "customers/{user_pk}/documents/{filename}".format(
        user_pk=instance.lead.pk, filename=filename
    )


class Contract(models.Model):
    name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_("Contract Name"),
        db_index=True,
    )
    product = models.OneToOneField(
        to=Product,
        on_delete=models.PROTECT,
        verbose_name=_("Service"),
        related_name="contract",
    )
    file_document = models.FileField(
        blank=False,
        null=False,
        upload_to=create_directory_path_for_documents_customer,
        verbose_name=_("Document file"),
    )
    start_date = models.DateField(
        blank=False,
        null=False,
        verbose_name=_("Start date"),
    )
    end_date = models.DateField(
        blank=False,
        null=False,
        verbose_name=_("End date"),
    )

    def __str__(self) -> str:
        return self.name
