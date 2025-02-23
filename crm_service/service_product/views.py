from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.db.models import QuerySet


from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import ProductCreateForm
from .models import Product


class ProductListView(ListView):
    """
    Представление для списка всех услуг.
    Пагинация настроена по выводу 10 услуг по умолчанию.
    Это можно изменить назначив paginate_by новое значение.
    Так же фильтрация стоит по не архивированным услугам.
    """

    permission_required = "service_product.view_product"
    model: Product = Product
    template_name: str = "service_product/products-list.html"
    queryset: QuerySet[Product, Product] = Product.objects.filter(archived=False)
    context_object_name: str = "products"
    paginate_by: int = 10


class ProductCreateView(CreateView):
    """Представление для создания услуги."""

    model: Product = Product
    form_class: ProductCreateForm = ProductCreateForm
    template_name: str = "service_product/products-create.html"

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном создании услуги, перенаправляет на страницу с деталями этой услуги."""
        return reverse_lazy(
            "service_product:service_detail", kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form: ProductCreateForm) -> HttpResponse:
        """
        Устанавливаем пользователя, создавшего услугу и дальше отправляем ответ с формы.
        """
        form.instance.created_by = User.objects.get(id=self.request.user.pk)
        return super().form_valid(form)


class ProductDetailView(DetailView):
    """Представление для отображения деталей услуги."""

    model: Product = Product
    template_name: str = "service_product/products-detail.html"
    context_object_name: str = "product"


class ProductUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    """Представление для редактирования данных об услуге."""

    permission_required = ("service_product.change_product",)
    model: Product = Product
    form_class: ProductCreateForm = ProductCreateForm
    template_name: str = "service_product/products-edit.html"

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном редактировании, перенаправляет на страницу с деталями этой услуги."""
        return reverse_lazy(
            "service_product:service_detail", kwargs={"pk": self.object.pk}
        )

    def test_func(self) -> bool:
        """
        Проверка прав доступа для изменения услуг, а точнее такие проверки:
            - если пользователь это суперюзер
            - если пользователь имеет права на изменения услуг
            иначе доступ будет закрыт.
        """
        self.object = self.get_object()
        if self.request.user.is_superuser or self.request.user.has_perm(
            "service_product.change_product"
        ):
            return True
        return False
