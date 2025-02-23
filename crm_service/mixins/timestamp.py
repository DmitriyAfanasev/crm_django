from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_%(class)s",
        verbose_name=_("created by"),
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_%(class)s",
        verbose_name=_("updated by"),
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self):
        return f"{self.__class__.__name__} created at {self.created_at}"
