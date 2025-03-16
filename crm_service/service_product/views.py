from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet


from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
)

from core.base import MyDeleteView
from .forms import ProductCreateForm
from .models import Product
from .dto_product import ProductCreateDTO, ProductUpdateDTO
from .services import ProductService


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Представление для списка всех услуг.
    Пагинация настроена по выводу 10 услуг по умолчанию.
    Это можно изменить назначив paginate_by новое значение.
    Так же фильтрация стоит по не архивированным услугам.
    """

    permission_required: str = "service_product.view_product"
    model: Product = Product
    template_name: str = "service_product/products-list.html"
    queryset: QuerySet[Product, Product] = Product.objects.filter(archived=False)
    context_object_name: str = "products"
    paginate_by: int = 10


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление для создания услуги."""

    permission_required: str = "service_product.create_product"
    model: Product = Product
    form_class: ProductCreateForm = ProductCreateForm
    template_name: str = "service_product/products-create.html"

    def form_valid(self, form: ProductCreateForm) -> HttpResponse:
        """
        Устанавливаем пользователя, создавшего услугу и делаем проверки различного уровня
         и создаём запись в базе данных.
        """

        user = User.objects.get(id=self.request.user.pk)
        dto = ProductCreateDTO(**form.cleaned_data, created_by=user)
        try:
            product = ProductService.create_product(dto)
        except ValidationError as error:
            form.add_error(error.code, error.message)
            return self.form_invalid(form)

        return redirect("service_product:service_detail", pk=product.pk)


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Представление для отображения деталей услуги."""

    permission_required: str = "service_product.view_product"
    model: Product = Product
    template_name: str = "service_product/products-detail.html"
    context_object_name: str = "product"


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление для редактирования данных об услуге."""

    permission_required: str = "service_product.change_product"
    model: type[Product] = Product
    form_class: ProductCreateForm = ProductCreateForm
    template_name: str = "service_product/products-edit.html"

    def form_valid(self, form: ProductCreateForm) -> HttpResponse:
        """
        Устанавливаем пользователя вносящего изменения, и обновляем данные об услуге.
        """
        user = User.objects.get(id=self.request.user.pk)
        dto = ProductUpdateDTO(**form.cleaned_data, updated_by=user, id=self.object.pk)
        try:
            product = ProductService.update_product(dto)
        except ValidationError as error:
            form.add_error(error.code, error.message)
            return self.form_invalid(form)

        return redirect("service_product:service_detail", pk=product.pk)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MyDeleteView):
    """
    Представление для подтверждения удаления услуги.
    """

    permission_required: str = "service_product.delete_product"
    model: Product = Product
    context_object_name: str = "product"
    success_url = reverse_lazy("service_product:service_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs) -> HttpResponse:
        return super().delete(request, *args, **kwargs)
