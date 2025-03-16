from django.core.exceptions import ValidationError
from django import forms

from core.base import BaseForm
from .models import Product
from .services import ProductService


class ProductCreateForm(BaseForm):
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

    def clean(self) -> dict:
        """Общая валидация формы."""
        cleaned_data = super().clean()
        cost = cleaned_data.get("cost")
        discount = cleaned_data.get("discount")
        status = cleaned_data.get("status")
        archived = cleaned_data.get("archived")

        try:
            if cost is not None and discount is not None:
                ProductService.validate_discount(cost, discount)
            if status is not None and archived is not None:
                ProductService.validate_status_and_archived(status, archived)
        except ValidationError as error:
            self.add_error(error.code, error.message)

        return cleaned_data
