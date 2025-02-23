from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product


@admin.action(description="Archived products")
def make_archived(
    modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet
) -> None:
    """Действие для админ панели для архивации услуги, удобно использовать вместо удаления."""
    queryset.update(archived=True)


@admin.action(description="Unarchived products")
def make_unarchived(
    modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet
) -> None:
    """Действие для разархивации услуг."""
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ модель для работы с услугами"""

    actions = [make_archived, make_unarchived]
    list_display = (
        "pk",
        "name",
        "description",
        "cost",
        "discount",
        "final_cost",
        "status",
        "archived",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
    list_display_links = ("pk", "name")
    ordering = ("pk",)
    search_fields = ("name", "description")
    list_filter = ("status", "archived")
    readonly_fields = ("final_cost",)

    fieldsets = [
        (None, {"fields": ("name", "description")}),
        (
            "Price options",
            {"fields": ("cost", "discount"), "classes": ("collapse", "wide")},
        ),
        ("Extra options", {"fields": ("status", "archived"), "classes": ("collapse",)}),
    ]

    def final_cost(self, obj: Product) -> float:
        """Рассчитывает итоговую стоимость с учётом скидки для отображения в админке."""
        return obj.final_cost

    final_cost.short_description = _("Final cost")
