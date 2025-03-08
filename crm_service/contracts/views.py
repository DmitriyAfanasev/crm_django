from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .forms import ContractForm
from .models import Contract


class ContractListView(ListView):
    model = Contract
    context_object_name = "contracts"
    paginate_by = 10


class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy("contracts:contract_list")

    @transaction.atomic
    def form_valid(self, form):
        return super().form_valid(form)


class ContractDetailView(DetailView):
    model = Contract
    context_object_name = "contract"
    form_class = ContractForm


class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name_suffix = "_edit"

    def get_success_url(self) -> HttpResponse:
        print(self.__class__.__name__)
        return reverse_lazy("contracts:contract_detail", kwargs={"pk": self.object.pk})

    @transaction.atomic
    def form_valid(self, form):
        return super().form_valid(form)


class ContractDeleteView(DeleteView):
    model = Contract
    context_object_name = "contract"
    success_url = reverse_lazy("contracts:contract_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
