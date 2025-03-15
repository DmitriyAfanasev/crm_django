from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from core.base import MyDeleteView
from .dto_contracts import ContractCreateDTO, ContractUpdateDTO
from .services import ContractService
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

    def form_valid(self, form: ContractForm) -> HttpResponse:
        """Обрабатывает валидную форму."""
        user = User.objects.get(id=self.request.user.pk)
        try:
            dto = ContractCreateDTO(**form.cleaned_data, created_by=user)
            contract = ContractService.create_contract(dto)
            return redirect("contracts:contract_detail", pk=contract.pk)
        except ValidationError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


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

    def get_form_kwargs(self) -> dict:
        """Добавление пользователя в kwargs формы."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form: ContractForm) -> HttpResponse:
        """Обрабатывает форму на корректность данных."""
        form.cleaned_data["updated_by"] = self.request.user
        try:
            dto = ContractUpdateDTO(**form.cleaned_data, id=self.object.pk)
            contract = ContractService.update_contract(dto)
            return redirect("contracts:contract_detail", pk=contract.pk)
        except ValidationError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


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
