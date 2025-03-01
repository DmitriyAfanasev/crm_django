from pathlib import Path

from django.conf import settings
from django.core.cache import cache

from exception.exc import ForbiddenWordException


class BadWordsMixin:
    @staticmethod
    def _load_bad_words() -> set[str]:
        """Загружает список запрещенных слов из файла."""

        file_with_words: Path = settings.BAD_WORDS_FILE
        with open(file=file_with_words, mode="r", encoding="utf-8") as file:
            return {word.strip().lower() for word in file.readlines()}

    @staticmethod
    def _check_for_bad_words(text: str, bad_words: set[str]) -> bool:
        """
        Проверяет, содержит ли текст запрещенные слова.
        Если есть пересечение, то вернёт True, что должно вызывать исключение.
        """
        text_lower: str = text.lower()
        new_text = set(text_lower.split())
        return not new_text.isdisjoint(bad_words)  # Проверяем на пересечение

    @staticmethod
    def _check_field_for_bad_words(
        field_name: str, text: str, bad_words: set[str]
    ) -> None:
        """Проверяет поле на наличие запрещенных слов и генерирует исключение с соответствующим сообщением."""
        if BadWordsMixin._check_for_bad_words(text, bad_words):
            raise ForbiddenWordException(field_name)

    @staticmethod
    def _get_bad_words() -> set[str]:
        """Получает список запрещенных слов из кэша или загружает его, если он отсутствует."""
        bad_words: set[str] | None = cache.get("bad_words")
        if bad_words is None:
            bad_words = BadWordsMixin._load_bad_words()
            cache.set("bad_words", bad_words, timeout=7200)
        return bad_words
