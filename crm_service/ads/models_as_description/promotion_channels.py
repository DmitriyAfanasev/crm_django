from django.db import models
from django.utils.translation import gettext_lazy as _


class PromotionChannel(models.Model):
    """
    Модель для каналов продвижения.

    Атрибуты:
        name (str): Название канала продвижения.
        description (str): Описание канала продвижения.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Channel Name"),
        help_text=_("The name of the promotion channel."),
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("A brief description of the promotion channel."),
    )

    def __str__(self) -> str:
        return self.name
