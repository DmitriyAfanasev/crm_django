import re
import logging

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from utils.mixins.services_mixins import BadWordsMixin
from .dto_product import ProductCreateDTO, ProductUpdateDTO
from .models import Product
from core.check_user_service import UserRoleService


logger = logging.getLogger("services")


class ProductService(BadWordsMixin, UserRoleService):

    @classmethod
    def create_product(cls, dto: ProductCreateDTO) -> Product:
        """Создание услуги."""
        try:
            cls.validate_product_data(dto)
        except ValidationError as error:
            logger.error(f"Validation error while creating product: {error}")
            raise

        with transaction.atomic():
            product = Product.objects.create(**dto.to_dict())
            product.save()

        return product

    @classmethod
    def update_product(cls, dto: ProductUpdateDTO) -> Product:
        """Обновление услуги"""
        try:
            cls.validate_product_data(dto)
        except ValidationError as error:
            logger.error(f"Validation error while creating product: {error}")
            raise

        with transaction.atomic():
            Product.objects.filter(id=dto.id).update(**dto.to_dict())
            product = Product.objects.get(id=dto.id)
            product.save()

        return product

    @classmethod
    def validate_name(cls, name: str) -> str:
        """Валидация имени услуги."""
        if len(name) < 3:
            raise ValidationError(
                _("Name must be at least 3 characters long."), code="name"
            )

        invalid_pattern = re.compile(r"[!@#$%^&*()\"`{}/\\]")
        invalid_chars = invalid_pattern.findall(name)
        if invalid_chars:
            raise ValidationError(
                _(
                    f"Name contains invalid characters: [ {'  '.join(set(invalid_chars))} ]"
                ),
                code="name",
            )

        if name.isdigit():
            raise ValidationError(
                _("The service name should not consist only of numbers."), code="name"
            )

        numbers_pattern = re.compile(r"\d+")
        numbers_found = numbers_pattern.findall(name)
        if len(numbers_found) > 1:
            raise ValidationError(
                _("Name must contain no more than one number."), code="name"
            )

        return name

    @classmethod
    def validate_description(cls, description: str) -> str:
        """Валидация описания услуги."""
        if len(description) < 10:
            raise ValidationError(
                _("Description must be at least 10 characters long."),
                code="description",
            )
        return description

    @classmethod
    def validate_cost(cls, cost: float) -> float:
        """Валидация стоимости услуги."""
        if cost < 0:
            raise ValidationError(_("Cost must be a positive number."), code="cost")
        elif cost == 0:
            raise ValidationError(_("Do you want to work for free?"), code="cost")
        return cost

    @classmethod
    def validate_discount(cls, cost: float, discount: int) -> None:
        """Проверяет корректность скидки."""
        if discount >= cost:
            raise ValidationError(
                _("Discount cannot be greater than or equal to cost."), code="discount"
            )

    @classmethod
    def validate_status_and_archived(cls, status: str, archived: bool) -> None:
        """Проверяет, что продукт не может быть одновременно активным и архивированным."""
        if archived and status == "active":
            raise ValidationError(
                _("Archived products cannot be active."), code="status"
            )

    @classmethod
    def validate_product_data(cls, dto: ProductCreateDTO | ProductUpdateDTO) -> None:
        """Проверяет данные перед созданием или обновлением услуги."""
        cls.validate_name(dto.name)
        cls.validate_description(dto.description)
        cls.validate_cost(dto.cost)
        cls.validate_discount(dto.cost, dto.discount)
        cls.validate_status_and_archived(dto.status, dto.archived)
