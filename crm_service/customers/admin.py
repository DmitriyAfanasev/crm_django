from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "lead",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "full_name",
    )
    list_display_links = (
        "pk",
        "lead",
    )
    search_fields = ("pk", "lead__first_name", "lead__last_name")

    @admin.display(description="Full name")
    def full_name(self, obj: Customer) -> str:
        return obj.lead.abbreviated_name
