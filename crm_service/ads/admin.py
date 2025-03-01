from django.utils.translation import gettext_lazy as _

from django.contrib import admin

from .models import AdsCompany


@admin.register(AdsCompany)
class AdsCompanyAdmin(admin.ModelAdmin):
    list_display = (
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
    )
    list_display_links = ("name",)
    list_filter = ("channel", "country", "created_at")
    search_fields = ("name", "email", "website")
    fieldsets = (
        (None, {"fields": ("name", "product", "channel", "budget")}),
        (_("Contact Info"), {"fields": ("country", "email", "website")}),
        (_("Creator"), {"fields": ("created_by",)}),
    )

    def calculate_roi(self, model: AdsCompany) -> str:
        """Отображает ROI в админке."""
        return f"{model.calculate_roi(10000):.2f}%"

    calculate_roi.short_description = _("ROI")

    def is_active(self, model: AdsCompany) -> str:
        """Отображает статус активности компании в админке."""
        return _("Active") if model.is_active() else _("Inactive")

    is_active.short_description = _("Status")
