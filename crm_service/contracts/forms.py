import datetime

from django.core.files import File
from django.utils.translation import gettext_lazy as _
from django import forms

from core.base import BaseForm

from .models import Contract
from .services import ContractService


class ContractForm(BaseForm):
    """Форма для создания и редактирования контракта."""

    class Meta:
        model = Contract
        fields = ("name", "product", "file_document", "start_date", "end_date", "cost")
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "file_document": forms.FileInput(attrs={"class": "form-control"}),
            "cost": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean_start_date(self) -> datetime.date:
        """Проверяет, что дата начала контракта указана."""
        start_date = self.cleaned_data.get("start_date")
        if start_date is None:
            raise forms.ValidationError(_("Start date is required."))
        return start_date

    def clean_end_date(self) -> datetime.date:
        """Проверяет, что дата окончания контракта указана."""
        end_date = self.cleaned_data.get("end_date")
        if end_date is None:
            raise forms.ValidationError(_("End date is required."))
        return end_date

    def clean(self) -> dict:
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            ContractService.validate_dates(start_date, end_date)

        return cleaned_data

    def clean_file_document(self) -> File:
        """
        Проверка, что файл подходящего расширения, и его размер не более 10 МБ (по умолчанию).
        """
        file_document: File = self.cleaned_data["file_document"]
        ContractService.validate_file(file_document)
        return file_document

    def clean_cost(self) -> float:
        """Проверяет, что стоимость контракта положительна."""
        cost: float = self.cleaned_data.get("cost")
        contract_pk = self.instance.pk
        if cost is None:
            raise forms.ValidationError(_("Cost is required."))
        ContractService.validate_cost(cost, contract_pk, user=self.user)
        return cost
