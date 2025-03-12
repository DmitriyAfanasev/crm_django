from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.db import transaction

from core.base import MyDeleteView
from leads.models import Lead
from .models import Customer
from .forms import CustomerForm


class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Представление списка всех активных клиентов."""

    permission_required: str = "view_customer"
    model: Customer = Customer
    context_object_name: str = "customers"
    paginate_by: int = 10
    ordering: tuple[str,] = ("contract__cost",)


class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представления для перевода лида в активного клиента."""

    permission_required: str = "view_customer"
    model: Customer = Customer
    form_class: CustomerForm = CustomerForm

    def get_initial(self) -> dict[str, Lead | None]:
        """Предзаполнение поля 'lead' значением из URL."""
        initial: dict = super().get_initial()
        lead_id: int | None = self.request.GET.get("lead_id")
        if lead_id:
            lead: Lead = get_object_or_404(Lead, pk=lead_id)
            initial["lead"] = lead
        return initial

    @transaction.atomic
    def form_valid(self, form: CustomerForm) -> HttpResponse:
        """Добавляет информацию о пользователе, который перевёл лида в активного клиента."""
        form.instance.created_by = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_success_url(self) -> HttpResponseRedirect:
        """Перенаправление на страницу деталей клиента."""
        return reverse_lazy("customers:customers_detail", kwargs={"pk": self.object.pk})


class CustomerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Представление для детального просмотра клиента."""

    permission_required: str = "view_customer"
    model: Customer = Customer
    context_object_name: str = "customer"


class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление для редактирования клиента."""

    permission_required: str = "change_customer"
    model: Customer = Customer
    context_object_name: str = "customer"
    form_class: CustomerForm = CustomerForm
    template_name_suffix: str = "_edit"

    @transaction.atomic
    def form_valid(self, form: CustomerForm) -> HttpResponse:
        """Добавляет информацию о пользователе, обновившего данные активного клиента."""
        response = super().form_valid(form)
        if form.is_valid():
            form.instance.updated_by = User.objects.get(pk=self.request.user.pk)
            return response

    def get_success_url(self) -> HttpResponseRedirect:
        """Перенаправление на страницу деталей клиента."""
        return reverse_lazy("customers:customers_detail", kwargs={"pk": self.object.pk})


class CustomerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MyDeleteView):
    """Представление для удаления клиента."""

    permission_required = "delete_customer"
    model: Customer = Customer
    success_url: str = reverse_lazy("customers:customers_list")

    @transaction.atomic
    def delete(self, request: HttpRequest, *args, **kwargs):
        """Обрабатывает запрос на удаление клиента."""
        return super().delete(request, *args, **kwargs)
