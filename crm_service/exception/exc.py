from django.core.exceptions import ValidationError


class ForbiddenWordException(ValidationError):
    def __init__(self, field_name: str):
        super().__init__(f"{field_name.capitalize()} contains forbidden words.")
