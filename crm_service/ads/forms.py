from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from django import forms
from poetry.console.commands import self

from .models import AdsCompany

if TYPE_CHECKING:
    from service_product.models import Product


class AdsCompanyCreateForm(forms.ModelForm):
    """Форма для создания рекламной компании."""

    class Meta:
        model = AdsCompany
        fields = ("name", "product", "channel", "budget", "country", "email", "website")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "channel": forms.Select(attrs={"class": "form-control"}),
            "budget": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "website": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_name(self) -> str:
        name: str = self.cleaned_data["name"]
        if len(name) < 3:
            raise forms.ValidationError(_("Name must be at least 3 characters long."))
        return name

    def clean_budget(self) -> float:
        budget: float = self.cleaned_data["budget"]
        product: Product = self.cleaned_data["product"]
        if budget < product.cost:
            raise forms.ValidationError(
                _("The budget cannot be less than the product cost.")
            )
        return budget

    def clean_country(self) -> str:
        country: str = self.cleaned_data["country"]
        if country is None:
            raise forms.ValidationError(_("Country must be provided."))
        return country

    def clean_website(self) -> str:
        website: str = self.cleaned_data["website"]
        if not website.startswith("https://") or not website.endswith("http://"):
            website = f"https://{website}"
        return website
