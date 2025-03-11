from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from pydantic import Field

from utils.mixins.services_mixins import BadWordsMixin
from .dto_product import ProductCreateDTO, ProductUpdateDTO
from .models import Product
from core.check_user_service import UserRoleService


# TODO можно будет добавить рейтинг для заказчиков, и если у них хороший рейтинг, делать скидку или брать их заказы из очереди первыми.
class ProductService(BadWordsMixin, UserRoleService):
    name: str = Field(min_length=3, max_length=100)
    description: str
    cost: float
    discount: int
    status: str
    archived: bool
    created_by: int

    @staticmethod
    def _check_name_uniqueness(
        name: str,
        error_message: str,
    ) -> None:
        """Проверяет уникальность имени поля в базе данных."""
        ProductService._check_existing_name_by_field_in_db(Product, name, error_message)

    @staticmethod
    def _check_discount(cost: float, discount: int) -> None:
        """Проверяет корректность скидки."""
        if discount >= cost:
            raise ValueError(_("Discount cannot be greater than or equal to cost."))

    @staticmethod
    def _check_status_and_archived(status: str, archived: bool) -> None:
        """
        Проверяет, что продукт не может быть одновременно активным и архивированным.
        """
        if archived and status == "active":
            raise ValueError(_("Archived products cannot be active."))

    @staticmethod
    def _check_user(user_id: int) -> None:
        """
        Проверяет активность и роль пользователя.

        :param user_id: ID пользователя.
        :raises ValueError: Если пользователь не существует или не имеет нужной роли.
        """
        ProductService._check_active_user(user_id=user_id)
        try:
            user = User.objects.get(id=user_id)
            service_name = ProductService._get_service_name()
            ProductService._check_user_role(user=user, service_name=service_name)
        except ObjectDoesNotExist:
            raise ValueError(_("User does not exist."))

    @staticmethod
    def checking_before_creation(data_from_request: ProductCreateDTO) -> None:
        """
        Проверяет данные перед созданием продукта.

        :param data_from_request: Данные для создания продукта.
        :raises ValueError: Если данные не прошли проверку.
        """
        bad_words: set[str] = ProductService._get_bad_words()

        ProductService._check_name_uniqueness(
            data_from_request.name, _("This service is already registered.")
        )
        ProductService._check_for_bad_words(data_from_request.name, bad_words)
        ProductService._check_for_bad_words(data_from_request.description, bad_words)
        ProductService._check_discount(
            data_from_request.cost, data_from_request.discount
        )
        ProductService._check_status_and_archived(
            data_from_request.status, data_from_request.archived
        )
        ProductService._check_user(data_from_request.created_by.pk)

    @staticmethod
    def checking_before_update(data_from_request: ProductUpdateDTO) -> None:
        current_product = Product.objects.get(pk=data_from_request.pk)

        if current_product.name != data_from_request.name:
            ProductService._check_name_uniqueness(
                data_from_request.name,
                _("This service is already registered."),
            )
        bad_words: set[str] = ProductService._get_bad_words()
        ProductService._check_for_bad_words(data_from_request.name, bad_words)
        ProductService._check_for_bad_words(data_from_request.description, bad_words)
        ProductService._check_discount(
            data_from_request.cost, data_from_request.discount
        )
        ProductService._check_status_and_archived(
            data_from_request.status, data_from_request.archived
        )
        ProductService._check_user(data_from_request.updated_by.pk)
