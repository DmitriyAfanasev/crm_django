from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)

from .models import AdsCompany
from .forms import AdsCompanyCreateForm


# TODO добавить пермишены
class AdsCompanyListView(ListView):
    """Представление для списка всех рекламных компаний в системе."""

    model: AdsCompany = AdsCompany


class AdsCompanyCreateView(CreateView):
    """Представление для маркетологов и всех у кого есть право на создание рекламных компаний."""

    model: AdsCompany = AdsCompany
    form_class: AdsCompanyCreateForm = AdsCompanyCreateForm

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном создании услуги, перенаправляет на страницу с деталями этой услуги."""
        return reverse_lazy("ads:ads_detail", kwargs={"pk": self.object.pk})


class AdsCompanyDetailView(DetailView):
    model: AdsCompany = AdsCompany
    context_object_name: str = "company"
