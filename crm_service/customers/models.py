from django.db import models
from django.db.models import BooleanField
from django.utils.translation import gettext_lazy as _

from contracts.models import Contract
from utils.mixins import TimestampMixin, ActorMixin
from leads.models import Lead


# Менеджер может создавать, просматривать и редактировать контракты, смотреть потенциальных клиентов и переводить их в активных.
class Customer(TimestampMixin, ActorMixin):
    """Активный клиент пользующийся услугами компаний."""

    lead: Lead = models.OneToOneField(
        blank=False,
        null=False,
        to=Lead,
        on_delete=models.PROTECT,
        related_name="customer",
        verbose_name=_("Lead"),
    )
    contract: Contract = models.ForeignKey(
        blank=False,
        null=False,
        to=Contract,
        on_delete=models.PROTECT,
        related_name="customer",
        verbose_name=_("Contract"),
    )
    archived: BooleanField = models.BooleanField(
        default=False, verbose_name=_("Archived")
    )

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = (
            "pk",
            "-created_at",
        )

    def __str__(self) -> str:
        return f"Customer: {self.lead.full_name}"
