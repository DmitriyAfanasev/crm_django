from django.utils.translation import gettext_lazy as _

from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):
    """Форма для создания услуг."""

    class Meta:
        model = Product
        fields = ("name", "description", "cost", "discount", "status", "archived")
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "cost": _("Cost"),
            "discount": _("Discount"),
            "status": _("Status"),
            "archived": _("Archived"),
        }
