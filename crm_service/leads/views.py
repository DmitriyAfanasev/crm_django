from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)

from core.base import MyDeleteView
from .models import Lead
from .forms import LeadForm


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

    @transaction.atomic
    def form_valid(self, form: LeadForm) -> HttpResponse:
        """Если форма валидна, то устанавливаем того, кто создал лида, и возвращаем ответ дальше."""
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном создании лида перенаправляет на страницу с деталями этого лида."""
        return reverse_lazy("leads:leads_detail", kwargs={"pk": self.object.pk})


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

    @transaction.atomic
    def form_valid(self, form: LeadForm) -> HttpResponse:
        """Если форма валидна, устанавливает того, кто проводит изменение данных."""
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном изменении лида перенаправляет на страницу с деталями этого лида."""
        return reverse_lazy("leads:leads_detail", kwargs={"pk": self.object.pk})


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
