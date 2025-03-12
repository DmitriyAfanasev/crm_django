from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import AdsCompany


@admin.register(AdsCompany)
class AdsCompanyAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели AdsCompany."""

    list_display: tuple = (
        "pk",
        "name",
        "product",
        "channel",
        "budget",
        "country",
        "email",
        "website",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
    list_display_links: tuple = ("name",)
    list_filter: tuple = ("channel", "country", "created_at")
    search_fields: tuple = ("name", "email", "website")
    fieldsets: tuple = (
        (None, {"fields": ("name", "product", "channel", "budget")}),
        (_("Contact Info"), {"fields": ("country", "email", "website")}),
        (_("Creator"), {"fields": ("created_by",)}),
    )
    readonly_fields: tuple = ("created_at", "updated_at", "created_by")
    date_hierarchy: str = "created_at"
