from pydantic import EmailStr

from service_product.models import Product
from dataclasses import dataclass


@dataclass
class AdsCompanyDTO:
    """DTO уже созданной модели, для передачи данных между другими слоями."""

    pk: int
    name: str
    product: Product
    channel: str
    budget: float
    country: str
    email: EmailStr
    created_by: int
    website: str


@dataclass
class AdsCompanyCreateDTO:
    """DTO для ещё не созданной записи в бд, передаётся в сервис для пред проверки."""

    name: str
    product: Product
    channel: str
    budget: float
    country: str
    email: EmailStr
    created_by: int
    website: str
