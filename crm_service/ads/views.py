from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    TemplateView,
)
from django.db import transaction

from .dto_ads_company import AdsCompanyCreateDTO
from .models import AdsCompany
from .forms import AdsCompanyCreateForm
from .services import AdsCompanyService


# TODO добавить пермишены
class AdsCompanyListView(ListView):
    """Представление для списка всех рекламных компаний в системе."""

    model: AdsCompany = AdsCompany
    context_object_name: str = "ads"
    paginate_by = 10
    ordering = ("budget",)


class AdsCompanyCreateView(PermissionRequiredMixin, CreateView):
    """Представление для маркетологов и всех у кого есть право на создание рекламных компаний."""

    model = AdsCompany
    form_class = AdsCompanyCreateForm
    permission_required = "ads.add_adscompany"

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном создании компании, перенаправляет на страницу с детальной информации о компании."""
        return reverse_lazy("ads:ads_detail", kwargs={"pk": self.object.pk})

    @transaction.atomic
    def form_valid(self, form: AdsCompanyCreateForm) -> HttpResponse:
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
        return super().form_valid(form)


class AdsCompanyDetailView(DetailView):
    model: AdsCompany = AdsCompany
    context_object_name: str = "company"


class AdsCompanyUpdateView(UpdateView):
    model: AdsCompany = AdsCompany
    form_class: AdsCompanyCreateForm = AdsCompanyCreateForm
    template_name_suffix = "-edit"

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном создании услуги, перенаправляет на страницу с деталями этой услуги."""
        return reverse_lazy("ads:ads_detail", kwargs={"pk": self.object.pk})

    @transaction.atomic
    def form_valid(self, form: AdsCompanyCreateForm) -> HttpResponse:
        return super().form_valid(form)


class AdsCompanyDeleteView(DeleteView):
    model: AdsCompany = AdsCompany

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном удалении компании, перенаправляет на страницу со списком компаний."""
        return reverse_lazy("ads:ads_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# TODO работает шаблон, но не логика которую он должен выводить
class AdsCompanyStatisticsView(ListView):
    template_name = "ads/adscompany_statistic.html"
    model = AdsCompany
    context_object_name = "ads"
