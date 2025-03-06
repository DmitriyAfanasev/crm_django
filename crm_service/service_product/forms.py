import re

from django.utils.translation import gettext_lazy as _

from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):
    """Форма для создания услуг."""

    class Meta:
        model = Product
        fields = ("name", "description", "cost", "discount", "status", "archived")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "cost": forms.NumberInput(attrs={"class": "form-control"}),
            "discount": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "archived": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "style": "box-shadow: 0 0 5px rgba(0,0,0,0.4);",
                }
            ),
        }

    def clean_name(self) -> str:
        name_service: str = self.cleaned_data["name"]
        if len(name_service) < 3:
            raise forms.ValidationError(_("Name must be at least 3 characters long."))

        invalid_pattern: re.Pattern = re.compile(r"[!@#$%^&*()\"`{}/\\]")
        invalid_chars: list[str] = invalid_pattern.findall(name_service)
        if invalid_chars:
            raise forms.ValidationError(
                _(
                    f"Name contains invalid characters: [ {'  '.join(set(invalid_chars))} ]"
                )
            )
        if name_service.isdigit():
            raise forms.ValidationError(
                _("The service name should not consist only of numbers.")
            )

        numbers_pattern = re.compile(r"\d+")
        numbers_found = numbers_pattern.findall(name_service)
        if len(numbers_found) > 1:
            raise forms.ValidationError(_("Name must contain no more than one number."))

        return name_service

    def clean_description(self) -> str:
        description_service: str = self.cleaned_data["description"]
        if len(description_service) < 10:
            raise forms.ValidationError(
                _("Description must be at least 10 characters long.")
            )
        return description_service

    def clean_cost(self) -> float:
        cost: float = self.cleaned_data["cost"]
        if cost < 0:
            raise forms.ValidationError(_("Cost must be a positive number."))
        elif cost == 0:
            raise forms.ValidationError(_("Do you want to work for free?"))
        return cost
