from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)
from django.db import transaction

from core.base import MyDeleteView
from .dto_ads_company import AdsCompanyCreateDTO
from .models import AdsCompany
from .forms import AdsCompanyCreateForm
from .services import AdsCompanyService


class AdsCompanyListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Представление для списка всех рекламных компаний в системе."""

    permission_required: str = "view_adscompany"
    model: AdsCompany = AdsCompany
    context_object_name: str = "ads"
    paginate_by: int = 10
    ordering: tuple[str,] = ("budget",)


class AdsCompanyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление для маркетологов и всех у кого есть право на создание рекламных компаний."""

    permission_required: str = "add_adscompany"
    model: AdsCompany = AdsCompany
    form_class: AdsCompanyCreateForm = AdsCompanyCreateForm

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном создании компании, перенаправляет на страницу с детальной информацией о компании."""
        return reverse_lazy("ads:ads_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form: AdsCompanyCreateForm) -> HttpResponse:
        """Проверка корректности данных из формы, а так же добавляет информацию
        о пользователе, который создаёт новую рекламную компанию."""
        form.instance.created_by = User.objects.get(id=self.request.user.pk)

        ads_company_dto = AdsCompanyCreateDTO(
            **form.cleaned_data,
            created_by=form.instance.created_by.pk,
        )
        try:
            AdsCompanyService.checking_before_creation(ads_company_dto)
        except ValueError as error:
            form.add_error(None, str(error))
            return self.form_invalid(form)

        with transaction.atomic():
            return super().form_valid(form)


class AdsCompanyDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Представление для детального просмотра рекламной компании."""

    permission_required: str = "view_company"
    model: AdsCompany = AdsCompany
    context_object_name: str = "company"


class AdsCompanyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление для редактирования рекламной компании."""

    permission_required: str = "change_adscompany"
    model: AdsCompany = AdsCompany
    form_class: AdsCompanyCreateForm = AdsCompanyCreateForm
    template_name_suffix: str = "-edit"

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном создании услуги, перенаправляет на страницу с деталями этой услуги."""
        return reverse_lazy("ads:ads_detail", kwargs={"pk": self.object.pk})

    @transaction.atomic
    def form_valid(self, form: AdsCompanyCreateForm) -> HttpResponse:
        """Обрабатывает валидную форму и сохраняет изменения."""
        return super().form_valid(form)


class AdsCompanyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MyDeleteView):
    """Представление для удаления рекламной компании."""

    permission_required: str = "delete_adscompany"
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
