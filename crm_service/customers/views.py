from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Customer
from .forms import CustomerCreateForm


class CustomerListView(ListView):
    model = Customer
    context_object_name = "customers"
    paginate_by = 10


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerCreateForm

    def form_valid(self, form: CustomerCreateForm) -> HttpResponse:
        form.instance.created_by = User.objects.get(pk=self.request.user.pk)
        # TODO DTO слой добавить
        return super().form_valid(form)

    def get_success_url(self) -> HttpResponseRedirect:
        return reverse_lazy("customers:customer_detail", kwargs={"pk": self.object.pk})


class CustomerDetailView(DetailView):
    model = Customer
    context_object_name = "customer"


class CustomerUpdateView(UpdateView):
    model = Customer
    context_object_name = "customer"
    form_class = CustomerCreateForm

    def form_valid(self, form: CustomerCreateForm) -> HttpResponse:
        response = super().form_valid(form)
        if form.is_valid():
            form.instance.updated_by = User.objects.get(pk=self.request.user.pk)
            return response

    def get_success_url(self) -> HttpResponseRedirect:
        return reverse_lazy("customers:customer_detail", kwargs={"pk": self.object.pk})
