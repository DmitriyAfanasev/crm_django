from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from pydantic import BaseModel, Field
from pathlib import Path

from .dto_product import ProductCreateDTO
from .models import Product


class BaseProduct(BaseModel): ...


# TODO можно будет добавить рейтинг для заказчиков, и если у них хороший рейтинг, делать скидку или брать их заказы из очереди первыми.
class ProductService(BaseProduct):
    name: str = Field(min_length=3, max_length=100)
    description: str
    cost: float
    discount: int
    status: str
    archived: bool
    created_by: int

    @staticmethod
    def _load_bad_words() -> set[str]:
        """Загружает список запрещенных слов из файла."""

        file_with_words: Path = settings.BAD_WORDS_FILE
        with open(file=file_with_words, mode="r", encoding="utf-8") as file:
            return {word.strip().lower() for word in file.readlines()}

    @staticmethod
    def _check_for_bad_words(text: str, bad_words: set[str]) -> bool:
        """Проверяет, содержит ли текст запрещенные слова."""
        text_lower: str = text.lower()
        new_text = set(text_lower.split())  # Преобразуем список слов в множество
        return not new_text.isdisjoint(bad_words)  # Проверяем на пересечение

    @staticmethod
    def checking_before_creation(data_from_request: ProductCreateDTO) -> None:
        """Проверяет данные перед созданием продукта."""

        if Product.objects.filter(name=data_from_request.name).exists():
            raise ValueError(_("This service is already registered."))

        if data_from_request.discount >= data_from_request.cost:
            raise ValueError(_("Discount cannot be greater than or equal to cost."))

        if data_from_request.archived and data_from_request.status == "active":
            raise ValueError(_("Archived products cannot be active."))

        creator = User.objects.filter(id=data_from_request.created_by, is_active=True)
        if not creator:
            raise ValueError(_("The creator must be an active user."))

        bad_words: set[str] | None = cache.get("bad_words")
        if bad_words is None:
            bad_words: set[str] = ProductService._load_bad_words()
            cache.set("bad_words", bad_words, timeout=7200)

        if ProductService._check_for_bad_words(data_from_request.name, bad_words):
            raise ValueError(_("Name contains forbidden words."))

        if ProductService._check_for_bad_words(
            data_from_request.description, bad_words
        ):
            raise ValueError(_("Description contains forbidden words."))
