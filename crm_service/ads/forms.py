from django import forms
from django.core.exceptions import ValidationError
from core.base import BaseForm

from .models import AdsCompany
from .services import AdsCompanyService


class AdsCompanyForm(BaseForm):
    """Форма для создания рекламной компании."""

    class Meta:
        model: AdsCompany = AdsCompany
        fields: tuple[str, ...] = (
            "name",
            "product",
            "budget",
            "country",
            "email",
            "website",
            "channel",
        )
        widgets: dict[str, forms.Widget] = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "budget": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "website": forms.TextInput(attrs={"class": "form-control"}),
            "channel": forms.Select(attrs={"class": "form-control"}),
        }

    def clean(self) -> dict:
        """Проверяет данные формы и передаёт их в сервис для валидации."""
        cleaned_data = super().clean()
        try:
            AdsCompanyService.validate_name(cleaned_data.get("name"))
            AdsCompanyService.validate_budget(
                cleaned_data.get("budget"), cleaned_data.get("product").cost
            )
            AdsCompanyService.validate_country(cleaned_data.get("country"))
            cleaned_data["website"] = AdsCompanyService.validate_website(
                cleaned_data.get("website")
            )
        except ValidationError as error:
            self.add_error(None, str(error))
        return cleaned_data
