from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from core.base import MyDeleteView
from .forms import ContractForm
from .models import Contract


class ContractListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Представление для отображения списка контрактов."""

    permission_required: str = "contracts.view_contract"
    model: Contract = Contract
    context_object_name: str = "contracts"
    paginate_by: int = 10
    ordering: tuple[str,] = ("-created_at",)


class ContractCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление для создания нового контракта."""

    permission_required: str = "contracts.add_contract"
    model: Contract = Contract
    form_class: ContractForm = ContractForm
    success_url: str = reverse_lazy("contracts:contract_list")

    @transaction.atomic
    def form_valid(self, form: ContractForm) -> HttpResponse:
        """Обрабатывает валидную форму."""
        return super().form_valid(form)


class ContractDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Представление для детального просмотра контракта."""

    permission_required: str = "contracts.view_contract"
    model: Contract = Contract
    context_object_name: str = "contract"
    form_class: ContractForm = ContractForm


class ContractUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление для редактирования контракта."""

    permission_required: str = "contracts.change_contract"
    model: Contract = Contract
    form_class: ContractForm = ContractForm
    template_name_suffix: str = "_edit"

    def get_success_url(self) -> str:
        """Возвращает URL для перенаправления после успешного редактирования."""
        return reverse_lazy("contracts:contract_detail", kwargs={"pk": self.object.pk})

    @transaction.atomic
    def form_valid(self, form: ContractForm) -> HttpResponse:
        """Обрабатывает форму на корректность данных."""
        return super().form_valid(form)


class ContractDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MyDeleteView):
    """Представление для удаления контракта."""

    permission_required: str = "contracts.delete_contract"
    model: Contract = Contract
    context_object_name: str = "contract"
    success_url: str = reverse_lazy("contracts:contract_list")

    @transaction.atomic
    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Обрабатывает запрос на удаление контракта."""
        return super().delete(request, *args, **kwargs)
