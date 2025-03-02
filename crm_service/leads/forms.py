from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "phone_number",
            "email",
            "campaign",
        )

        # TODO добавить валидацию формы
