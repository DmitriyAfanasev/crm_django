from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.db import models
from django.views.generic import ListView

from .models import Product


class ProductListView(ListView):
    """
    Представление для списка всех услуг.
    Пагинация настроена по выводу 10 услуг по умолчанию.
    Это можно изменить назначив paginate_by новое значение.
    Так же фильтрация стоит по не архивированным услугам.
    """

    model: models.Model = Product
    template_name: str = "service_product/products-list.html"
    queryset: QuerySet[Product, Product] = Product.objects.filter(archived=False)
    context_object_name: str = "products"
    paginator_class: Paginator = Paginator
    paginate_by: int = 10
