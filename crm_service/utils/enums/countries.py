from enum import Enum
from django.utils.translation import gettext_lazy as _
from typing import List, Tuple, TypeAlias

CountryCode: TypeAlias = str
NameOfCountry: TypeAlias = str
CountryChoices: TypeAlias = List[Tuple[CountryCode, NameOfCountry]]


class Country(Enum):
    RU = _("Russia")
    US = _("United States")
    CN = _("China")
    DE = _("Germany")
    FR = _("France")
    KZ = _("The Republic of Kazakhstan")

    @classmethod
    def choices(cls) -> CountryChoices:
        """Возвращает список кортежей (код страны, название страны) для использования в полях выбора."""
        return [(country.name, country.value) for country in cls]
