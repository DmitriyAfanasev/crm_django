from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)

from core.base import MyDeleteView
from .dto_lead import LeadCreateDTO, LeadUpdateDTO
from .models import Lead
from .forms import LeadForm
from .services import LeadService


class LeadListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Представление для списка лидов."""

    permission_required: str = "leads.view_lead"
    model: Lead = Lead
    context_object_name: str = "leads"
    paginate_by: int = 10
    ordering: tuple[str,] = ("-created_at",)


class LeadCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление для создания нового лида."""

    permission_required: str = "leads.add_lead"
    model: Lead = Lead
    form_class: LeadForm = LeadForm

    def form_valid(self, form: LeadForm) -> HttpResponse:
        """Если форма валидна, то устанавливаем того, кто создал лида, и возвращаем ответ дальше."""
        user = User.objects.get(id=self.request.user.pk)
        dto = LeadCreateDTO(**form.cleaned_data, created_by=user)
        try:
            lead = LeadService.create_lead(dto)
        except ValidationError as error:
            form.add_error(None, str(error))
            return self.form_invalid(form)

        return redirect("leads:leads_detail", pk=lead.pk)


class LeadDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Представление для отображения деталей лида."""

    permission_required = "leads.view_lead"
    model: Lead = Lead
    context_object_name: str = "lead"


class LeadUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление для обновления информации о лиде."""

    permission_required: str = "leads.change_lead"
    model: Lead = Lead
    context_object_name: str = "lead"
    form_class: LeadForm = LeadForm
    template_name_suffix: str = "_edit"

    def form_valid(self, form: LeadForm) -> HttpResponse:
        """Если форма валидна, устанавливает того, кто проводит изменение данных."""
        user = User.objects.get(id=self.request.user.pk)
        dto = LeadUpdateDTO(**form.cleaned_data, updated_by=user, id=self.object.pk)
        try:
            lead = LeadService.update_lead(dto)
        except ValidationError as error:
            form.add_error(None, str(error))
            return self.form_invalid(form)

        return redirect("leads:leads_detail", pk=lead.pk)


class LeadDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MyDeleteView):
    """Представление для удаления лида."""

    permission_required = "leads.delete_lead"
    model = Lead
    context_object_name = "lead"
    success_url = reverse_lazy("leads:leads_list")

    @transaction.atomic
    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Удаляет лида и возвращает ответ."""
        return super().delete(request, *args, **kwargs)
