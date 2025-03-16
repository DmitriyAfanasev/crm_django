from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления объектами Customer.

    Этот класс настраивает отображение и функциональность модели Customer
    в админ-панели Django.
    """

    list_display: tuple = (
        "pk",
        "lead",
        "archived",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "full_name",
    )
    list_display_links: tuple = (
        "pk",
        "lead",
    )
    search_fields: tuple = ("pk", "lead__first_name", "lead__last_name")
    list_filter: tuple = ("archived", "created_by", "updated_by")
    ordering: tuple = ("-created_at",)

    @admin.display(description="Full name")
    def full_name(self, obj: Customer) -> str:
        """Возвращает полное имя клиента, если lead существует, иначе 'N/A'."""
        return obj.lead.full_name if obj.lead else "N/A"
