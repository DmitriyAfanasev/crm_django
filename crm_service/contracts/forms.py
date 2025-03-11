import datetime

from django.core.files import File
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Contract


class ContractForm(forms.ModelForm):
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
        """Проверка, что дата начала договора не раньше, чем сегодня."""
        start_date = self.cleaned_data["start_date"]
        if start_date < datetime.date.today():
            raise forms.ValidationError(
                _("The contract cannot be started earlier than today")
            )

        return start_date

    def clean(self) -> dict:
        """
        Проверка, что день окончания договора не меньше, чем начало.
        А так же длительности контракта, он не может длиться меньше,
        чем один день, но и не больше 5 лет (по умолчанию).
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date < start_date:
            raise forms.ValidationError(
                _("The end of the contract cannot be earlier than its beginning")
            )

        min_duration = datetime.timedelta(days=1)
        if (end_date - start_date) <= min_duration:
            raise forms.ValidationError(
                _("The contract duration must be at least 1 day.")
            )

        # Проверка максимальной длительности (5 лет)
        max_duration = datetime.timedelta(days=365 * 5)
        if (end_date - start_date) > max_duration:
            raise forms.ValidationError(
                _("The contract duration cannot exceed 5 years.")
            )

        return cleaned_data

    def clean_file_document(self) -> File:
        """
        Проверка, что файл подходящего расширения, а так же его размер не более 10 МБ (по умолчанию).
        """
        file_document: File = self.cleaned_data["file_document"]
        allowed_extensions = [
            ".pdf",
            ".docx",
        ]
        if not any(
            file_document.name.lower().endswith(extension)
            for extension in allowed_extensions
        ):
            raise forms.ValidationError(_("Only PDF and DOCX files are allowed."))

        max_size = 10 * 1024 * 1024  # 10 МБ
        if file_document.size > max_size:
            raise forms.ValidationError(
                _("The file size cannot exceed {} MB. Your file size: {} MB").format(
                    max_size // (1024 * 1024), file_document.size // (1024 * 1024)
                )
            )
        return file_document

    def clean_cost(self) -> float:
        cost = self.cleaned_data["cost"]
        if cost <= 0:
            raise forms.ValidationError(_("The cost is invalid."))
        return cost
