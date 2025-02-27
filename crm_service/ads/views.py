from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)

from .models import AdsCompany
from .forms import AdsCompanyCreateForm


class AdsCompanyListView(ListView):
    model: AdsCompany = AdsCompany


class AdsCompanyCreateView(CreateView):
    model: AdsCompany = AdsCompany
    form_class = AdsCompanyCreateForm
