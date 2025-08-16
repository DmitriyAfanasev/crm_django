from enum import Enum
from typing import List, Tuple, TypeAlias

from django.utils.translation import gettext_lazy as _


CountryCode: TypeAlias = str
NameOfCountry: TypeAlias = str
CountryChoices: TypeAlias = List[Tuple[CountryCode, NameOfCountry]]


class Country(Enum):
    """Страны, которые обслуживает наш сервис."""

    RU = _("Russia")
    US = _("United States")
    CN = _("China")
    DE = _("Germany")
    FR = _("France")
    KZ = _("The Republic of Kazakhstan")

    @classmethod
    def choices(cls) -> CountryChoices:
        """Возвращает список кортежей для использования в полях выбора."""
        return [(country.name, country.value) for country in cls]


class RatingChoice(Enum):
    """
    Перечисление для возможных значений оценки.
    """

    ZERO = 0, _("0 - Poor")
    ONE = 1, _("1 - Below Average")
    TWO = 2, _("2 - Average")
    THREE = 3, _("3 - Good")
    FOUR = 4, _("4 - Very Good")
    FIVE = 5, _("5 - Excellent")

    @classmethod
    def choices(cls) -> list[tuple[int | None, str]]:
        """
        Возвращает список кортежей (значение, описание) для использования в полях выбора.
        """
        return [(rating.value[0], rating.value[1]) for rating in cls]

    @classmethod
    def get_rating_value(cls, rating: "RatingChoice") -> int | None:
        """
        Возвращает числовое значение оценки.
        """
        return rating.value[0]
