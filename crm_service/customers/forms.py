from django import forms
from django.apps import apps
from .models import Customer


class CustomerForm(forms.ModelForm):
    """Форма для перевода лида в активного клиента."""

    class Meta:
        model = Customer
        fields = ("lead", "contract")
        widgets = {
            "lead": forms.Select(attrs={"class": "form-control"}),
            "contract": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs) -> None:
        """Инициализация формы."""
        super().__init__(*args, **kwargs)
        Lead = apps.get_model("leads", "Lead")

        leads = Lead.objects.filter(customer__isnull=True)
        if not leads.exists():
            self.fields["lead"].help_text = "Нет доступных лидов для создания клиента."

        self.fields["lead"].queryset = leads
