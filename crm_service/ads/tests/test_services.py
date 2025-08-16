import pytest
import requests
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.apps import apps


from ads.dto_ads_company import AdsCompanyCreateDTO
from ads.services import AdsCompanyService

AdsCompany = apps.get_model("ads", "AdsCompany")
User = get_user_model()
PromotionChannel = apps.get_model("ads", "PromotionChannel")
Product = apps.get_model("service_product", "Product")
_service_company = AdsCompanyService()


# @pytest.fixture
# def test_user(db):
#     """Fixture for creating a test user."""
#     return User.objects.create(username="test_user", password="test_password")
#
#
# @pytest.mark.django_db
# def test_user_creation(test_user):
#     """Test that the user is created successfully."""
#     assert test_user.username == "test_user"
#     assert test_user.check_password("test_password")
#
#
#
@pytest.fixture
def test_company(test_user):
    """Фикстура для создания тестовой компании."""
    channel = PromotionChannel.objects.create(name="Test Channel")
    product = Product.objects.create(name="Test Product", cost=100.0)
    return AdsCompany.objects.create(
        name="Test Company",
        budget=1000.0,
        country="Russia",
        website="https://example.com",
        email="example@gmail.com",
        channel=channel,
        product=product,
        created_by=test_user,
    )


def test_validate_name_valid() -> None:
    _service_company.validate_name("Valid Name")


def test_validate_name_invalid() -> None:
    with pytest.raises(ValidationError):
        _service_company.validate_name("A")


def test_validate_budget_valid():
    budget = 100
    product_cost = 99
    _service_company.validate_budget(budget=budget, product_cost=product_cost)
    product_cost = 100
    _service_company.validate_budget(budget=budget, product_cost=product_cost)


def test_validate_budget_invalid():
    budget = 100
    product_cost = 101
    with pytest.raises(ValidationError):
        _service_company.validate_budget(budget=budget, product_cost=product_cost)


def test_validate_website_valid() -> None:
    website = "https://example.com"
    _service_company.validate_website(website=website)
    website_1 = "example.com"
    _service_company.validate_website(website=website)
    assert website == _service_company.validate_website(website=website_1)


def test_validate_website_invalid() -> None:
    with pytest.raises(ValidationError):
        website = "http://www.example.com"
        _service_company.validate_website(website=website)


# def test_create_company() -> None:
#     dto = AdsCompanyCreateDTO(
#         name="New Company",
#         budget=1000.0,
#         country="Russia",
#         website="https://example.com",
#         product=None,
#         created_by=None,
#     )
#     company = AdsCompanyService.create_company(dto)
#     _service_company.create_company()
#
#
# def test_check_existing_name() -> None:
#     _service_company._check_existing_name_by_field_in_db(
#         AdsCompany,
#     )
#
#
# def test_validate_common_fields() -> None:
#     test_validate_name_valid()
