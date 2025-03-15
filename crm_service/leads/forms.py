from django.utils.translation import gettext_lazy as _
from django import forms

from core.base import BaseForm
from .models import Lead


class LeadForm(BaseForm):
    """Форма для создания лида или обновления информации о нём."""

    class Meta:
        model = Lead
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "phone_number",
            "campaign",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+7 (___) ___-__-__",
                }
            ),
            "campaign": forms.Select(attrs={"class": "form-control"}),
        }

    @staticmethod
    def validate_name(name: str, field_name: str) -> str:
        """Вспомогательный метод для проверки имени или фамилии."""
        if len(name.split(" ")) > 1:
            raise forms.ValidationError(
                _(
                    f"{field_name} должно состоять из одного слова или быть разделено '-'"
                )
            )
        if len(name) < 2:
            raise forms.ValidationError(
                _(f"{field_name} должно содержать как минимум 2 символа")
            )
        return name

    def clean_first_name(self) -> str:
        """Валидация имени."""
        first_name: str = self.cleaned_data.get("first_name")
        return self.validate_name(first_name, "Имя")

    def clean_middle_name(self) -> str:
        """Валидация отчества."""
        middle_name: str = self.cleaned_data.get("middle_name", "")
        if middle_name:
            return self.validate_name(middle_name, "Отчество")
        return middle_name

    def clean_last_name(self) -> str:
        """Валидация фамилии."""
        last_name: str = self.cleaned_data.get("last_name")
        return self.validate_name(last_name, "Фамилия")
