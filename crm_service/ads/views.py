from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)
from django.db import transaction

from core.base import MyDeleteView
from .dto_ads_company import AdsCompanyCreateDTO, AdsCompanyUpdateDTO
from .models import AdsCompany
from .forms import AdsCompanyForm
from .services import AdsCompanyService


class AdsCompanyListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Представление для списка всех рекламных компаний в системе."""

    permission_required: str = "ads.view_adscompany"
    model: AdsCompany = AdsCompany
    context_object_name: str = "ads"
    paginate_by: int = 10
    ordering: tuple[str,] = ("budget",)


class AdsCompanyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление для маркетологов и всех у кого есть право на создание рекламных компаний."""

    permission_required: str = "ads.add_adscompany"
    model: AdsCompany = AdsCompany
    form_class: AdsCompanyForm = AdsCompanyForm

    def form_valid(self, form: AdsCompanyForm) -> HttpResponse:
        """Проверка корректности данных из формы, а так же добавляет информацию
        о пользователе, который создаёт новую рекламную компанию."""
        user = User.objects.get(id=self.request.user.pk)
        ads_company_dto = AdsCompanyCreateDTO(
            **form.cleaned_data,
            created_by=user,
        )
        try:
            company = AdsCompanyService.create_company(dto=ads_company_dto)
        except ValidationError as error:
            form.add_error(None, str(error))
            return self.form_invalid(form)

        return redirect("ads:ads_detail", pk=company.pk)


class AdsCompanyDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Представление для детального просмотра рекламной компании."""

    permission_required: str = "ads.view_adscompany"
    model: AdsCompany = AdsCompany
    context_object_name: str = "company"


class AdsCompanyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление для редактирования рекламной компании."""

    permission_required: str = "ads.change_adscompany"
    model: AdsCompany = AdsCompany
    form_class: AdsCompanyForm = AdsCompanyForm
    template_name_suffix: str = "-edit"

    def form_valid(self, form: AdsCompanyForm) -> HttpResponse:
        """Обрабатывает валидную форму и сохраняет изменения."""
        user = User.objects.get(id=self.request.user.pk)
        ads_company_dto = AdsCompanyUpdateDTO(
            **form.cleaned_data, updated_by=user, id=self.object.pk
        )
        try:
            company = AdsCompanyService.update_company(dto=ads_company_dto)
        except ValidationError as error:
            form.add_error(None, str(error))
            return self.form_invalid(form)

        return redirect("ads:ads_detail", pk=company.pk)


class AdsCompanyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MyDeleteView):
    """Представление для удаления рекламной компании."""

    permission_required: str = "ads.delete_adscompany"
    model: AdsCompany = AdsCompany
    success_url = reverse_lazy("ads:ads_list")

    @transaction.atomic
    def delete(self, request: HttpRequest, *args, **kwargs):
        """Удаляет рекламную компанию и перенаправляет на страницу со списком."""
        return super().delete(request, *args, **kwargs)


class AdsCompanyStatisticsView(LoginRequiredMixin, ListView):
    """Представление для статистики рекламных компаний."""

    template_name: str = "ads/adscompany_statistic.html"
    model: AdsCompany = AdsCompany
    context_object_name: str = "ads"
