from django import forms

from .models import AdsCompany


class AdsCompanyCreateForm(forms.ModelForm):
    """Форма для создания рекламной компании."""

    class Meta:
        model = AdsCompany
        fields = ("name", "product", "channel", "budget", "country", "email", "website")
