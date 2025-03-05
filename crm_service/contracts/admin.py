from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "product",
        "cost",
        "start_date",
        "end_date",
        "file_document",
    )
    search_fields = ("name",)
    list_display_links = ("name",)