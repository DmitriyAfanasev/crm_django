"""
Модуль создан лишь для практики реализации паттерна 'Репозиторий'.
Не нашёл ни одной причины по которой он тут будет уместен, поэтому
"""

from typing import Optional
from abc import ABC, abstractmethod

from .models import Product
from .dto_product import ProductDTO, ProductCreateDTO, ProductUpdateDTO


class AbstractProductRepository(ABC):
    """Абстрактный класс для репозитория продуктов."""

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self) -> list[Product]:
        pass

    @abstractmethod
    def create(self, product_data: ProductCreateDTO) -> Product:
        pass

    @abstractmethod
    def update(
        self, product_id: int, product_data: ProductUpdateDTO
    ) -> Optional[Product]:

        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:

        pass


class ProductRepository(AbstractProductRepository):
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Возвращает продукт по его ID."""
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def get_all(self) -> list[Product]:
        """Возвращает список всех продуктов."""
        return list(Product.objects.all())

    def create(self, product_data: ProductCreateDTO) -> Product:
        """Создает новый продукт."""
        return Product.objects.create(**product_data.to_dict())

    def update(
        self, product_id: int, product_data: ProductUpdateDTO
    ) -> Optional[Product]:
        """Обновляет данные продукта."""
        try:
            product = Product.objects.get(id=product_id)
            for attr, value in product_data.to_dict().items():
                setattr(product, attr, value)
            product.save()
            return product
        except Product.DoesNotExist:
            return None

    def delete(self, product_id: int) -> bool:
        """Удаляет продукт по его ID."""
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return True
        except Product.DoesNotExist:
            return False
