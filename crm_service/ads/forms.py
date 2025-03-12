from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from django import forms

from .models import AdsCompany

if TYPE_CHECKING:
    from service_product.models import Product


class AdsCompanyCreateForm(forms.ModelForm):
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

    def clean_name(self) -> str:
        """Проверяет, что имя рекламной компании не короче 3 символов."""
        name: str = self.cleaned_data["name"]
        if len(name) < 3:
            raise forms.ValidationError(_("Name must be at least 3 characters long."))
        return name

    def clean_budget(self) -> float:
        """Проверяет, что бюджет не меньше стоимости услуги."""
        budget: float = self.cleaned_data["budget"]
        product: Product = self.cleaned_data["product"]
        if budget < product.cost:
            raise forms.ValidationError(
                _("The budget cannot be less than the product cost.")
            )
        return budget

    def clean_country(self) -> str:
        """Проверяет, что страна указана."""
        country: str = self.cleaned_data["country"]
        if country is None:
            raise forms.ValidationError(_("Country must be provided."))
        return country

    def clean_website(self) -> str:
        """Проверяет, что веб-сайт начинается с HTTPS."""
        website: str = self.cleaned_data["website"]
        if website.startswith("http://"):
            raise forms.ValidationError(_("Website must be secure (use HTTPS)."))
        if not website.startswith("https://"):
            website = f"https://{website}"
        return website
