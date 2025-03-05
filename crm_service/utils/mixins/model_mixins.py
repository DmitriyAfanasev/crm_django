from django.db.models import ForeignKey, DateTimeField, Index
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class TimestampMixin(models.Model):
    """
    Миксин для добавления полей отслеживания создания и обновления моделей,
    а также отслеживания, кто создаёт и обновляет модель.

    Атрибуты:
        created_at (DateTimeField): Дата и время создания объекта
        updated_at (DateTimeField): Дата и время последнего обновления объекта
        created_by (ForeignKey): Пользователь, создавший объект
        updated_by (ForeignKey): Пользователь, обновивший объект
    """

    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: DateTimeField = models.DateTimeField(auto_now=True)
    created_by: ForeignKey | None = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_%(class)s",
        verbose_name=_("created by"),
    )
    updated_by: ForeignKey | None = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_%(class)s",
        verbose_name=_("updated by"),
    )

    class Meta:
        """
        Мета информация.
        Ключевым является комментарий, чтобы указать, что это мета-опции для абстрактного класса.
        """

        abstract: bool = True
        indexes: list[Index] = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.__class__.__name__} created at {self.created_at}"


class ActorMixin(models.Model):
    """
    Миксин для добавления полей отслеживания пользователей, создавших и обновивших модель.

    Атрибуты:
        created_by (ForeignKey): Пользователь, создавший объект.
        updated_by (ForeignKey): Пользователь, обновивший объект.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_%(class)s",
        verbose_name=_("created by"),
        help_text=_("The user who created the object."),
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_%(class)s",
        verbose_name=_("updated by"),
        help_text=_("The user who last updated the object."),
    )

    class Meta:
        abstract = True
