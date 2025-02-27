from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    TemplateView,
)

from .models import AdsCompany
from .forms import AdsCompanyCreateForm


# TODO добавить пермишены
class AdsCompanyListView(ListView):
    """Представление для списка всех рекламных компаний в системе."""

    model: AdsCompany = AdsCompany
    context_object_name: str = "ads"


class AdsCompanyCreateView(CreateView):
    """Представление для маркетологов и всех у кого есть право на создание рекламных компаний."""

    model: AdsCompany = AdsCompany
    form_class: AdsCompanyCreateForm = AdsCompanyCreateForm

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном создании компании, перенаправляет на страницу с детальной информации о компании."""
        return reverse_lazy("ads:ads_detail", kwargs={"pk": self.object.pk})


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


class AdsCompanyDeleteView(DeleteView):
    model: AdsCompany = AdsCompany

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном удалении компании, перенаправляет на страницу со списком компаний."""
        return reverse_lazy("ads:ads_list")


class AdsCompanyStatisticsView(TemplateView):
    template_name = "ads/adscompany_statistic.html"
