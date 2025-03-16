from typing import TYPE_CHECKING
from functools import cached_property
from django import forms

from core.base import BaseForm
from .models import Lead


if TYPE_CHECKING:
    from ads.models import AdsCompany
    from .services import LeadService


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
                    "placeholder": "+7 (***) ***-**-**",
                }
            ),
            "campaign": forms.Select(attrs={"class": "form-control"}),
        }

    @cached_property
    def _service(self) -> "LeadService":
        """Мягкий импорт класса-сервиса для обработки бизнес-логики."""
        from .services import LeadService

        return LeadService()

    def clean_first_name(self) -> str:
        """Валидация имени."""
        first_name: str = self.cleaned_data.get("first_name")
        return self._service.validate_name(first_name, "First Name")

    def clean_middle_name(self) -> str:
        """Валидация отчества."""
        middle_name: str = self.cleaned_data.get("middle_name", "")
        if middle_name:
            return self._service.validate_name(middle_name, "Middle Name")
        return middle_name

    def clean_last_name(self) -> str:
        """Валидация фамилии."""
        last_name: str = self.cleaned_data.get("last_name")
        return self._service.validate_name(last_name, "Last Name")

    def clean_email(self) -> str:
        """Валидация электронной почты."""
        email: str = self.cleaned_data.get("email")
        return self._service.validate_email(email)

    def clean_phone_number(self) -> str:
        """Валидация номера телефона."""
        phone_number: str = self.cleaned_data.get("phone_number")
        return self._service.validate_phone_number(phone_number)

    def clean_campaign(self) -> "AdsCompany":
        """Валидация рекламной компании."""
        campaign = self.cleaned_data.get("campaign")
        return self._service.validate_campaign(campaign)
