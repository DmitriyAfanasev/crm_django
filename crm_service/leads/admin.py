from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления экземплярами Lead.

    Этот класс настраивает административный интерфейс для модели Lead,
    позволяя легко управлять записями лидов.
    """

    list_display: tuple = (
        "first_name",
        "middle_name",
        "last_name",
        "phone_number",
        "email",
        "campaign",
        "is_active",
    )

    search_fields: tuple = ("first_name", "last_name", "email", "phone_number")
    list_filter: tuple = ("is_active", "campaign")
    ordering: tuple = ("last_name", "first_name")

    def full_name(self, obj: Lead) -> str:
        """Возвращает полное имя лида."""
        return obj.full_name

    full_name.short_description = "Full name"
