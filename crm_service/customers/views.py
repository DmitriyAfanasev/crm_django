from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db import transaction

from leads.models import Lead
from .models import Customer
from .forms import CustomerCreateForm


# TODO добавить пермишены
class CustomerListView(ListView):
    model = Customer
    context_object_name = "customers"
    paginate_by = 10


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerCreateForm

    def get_initial(self) -> dict[str, Lead]:
        """Предзаполнение поля 'lead' значением из URL."""
        initial = super().get_initial()
        lead_id = self.request.GET.get("lead_id")
        if lead_id:
            lead = get_object_or_404(Lead, pk=lead_id)
            initial["lead"] = lead
        return initial

    @transaction.atomic
    def form_valid(self, form: CustomerCreateForm) -> HttpResponse:
        form.instance.created_by = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_success_url(self) -> HttpResponseRedirect:
        return reverse_lazy("customers:customers_detail", kwargs={"pk": self.object.pk})


class CustomerDetailView(DetailView):
    model = Customer
    context_object_name = "customer"


class CustomerUpdateView(UpdateView):
    model = Customer
    context_object_name = "customer"
    form_class = CustomerCreateForm
    template_name_suffix = "_edit"

    @transaction.atomic
    def form_valid(self, form: CustomerCreateForm) -> HttpResponse:
        response = super().form_valid(form)
        if form.is_valid():
            form.instance.updated_by = User.objects.get(pk=self.request.user.pk)
            return response

    def get_success_url(self) -> HttpResponseRedirect:
        return reverse_lazy("customers:customers_detail", kwargs={"pk": self.object.pk})


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy("customers:customers_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
