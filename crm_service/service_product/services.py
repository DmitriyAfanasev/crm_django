from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from pydantic import Field

from utils.mixins.services_mixins import BadWordsMixin
from .dto_product import ProductCreateDTO
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
    def checking_before_creation(data_from_request: ProductCreateDTO) -> None:
        ProductService._check_existing_name_by_field_in_db(
            Product, data_from_request.name, _("This service is already registered.")
        )

        bad_words: set[str] = ProductService._get_bad_words()

        ProductService._check_field_for_bad_words(
            "name",
            data_from_request.name,
            bad_words,
        )
        ProductService._check_field_for_bad_words(
            "description",
            data_from_request.description,
            bad_words,
        )
        if data_from_request.discount >= data_from_request.cost:
            raise ValueError(_("Discount cannot be greater than or equal to cost."))

        if data_from_request.archived and data_from_request.status == "active":
            raise ValueError(_("Archived products cannot be active."))

        ProductService._check_active_user(user_id=data_from_request.created_by)

        user = User.objects.get(id=data_from_request.created_by)
        service_name = ProductService._get_service_name()
        ProductService._check_user_role(user=user, service_name=service_name)
