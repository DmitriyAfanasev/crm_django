from django.contrib import admin
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Contract."""

    list_display: tuple = (
        "pk",
        "name",
        "product",
        "cost",
        "start_date",
        "end_date",
        "file_document",
    )
    search_fields: tuple = ("name",)
    list_display_links: tuple = ("name",)
    list_filter: tuple = ("start_date", "end_date", "product")
    readonly_fields: tuple = ("created_at", "updated_at")
    date_hierarchy: str = "start_date"
