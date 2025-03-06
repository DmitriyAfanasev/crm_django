from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from customers.models import Customer
from .models import Lead
from .forms import LeadForm


class LeadListView(ListView):
    model = Lead
    context_object_name = "leads"
    paginate_by = 10
    queryset = Lead.objects.all()


class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm

    def form_valid(self, form: LeadForm) -> HttpResponse:
        form.instance.created_by = User.objects.get(pk=self.request.user.pk)

        # добавить слой DTO
        return super().form_valid(form)

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном создании лида, перенаправляет на страницу с деталями этого лида."""
        return reverse_lazy("leads:leads_detail", kwargs={"pk": self.object.pk})


class LeadDetailView(DetailView):
    model = Lead
    context_object_name = "lead"


class LeadUpdateView(UpdateView):
    model = Lead
    context_object_name = "lead"
    form_class = LeadForm
    template_name_suffix = "_edit"

    def form_valid(self, form: LeadForm) -> HttpResponse:
        """Если форма валидна, то устанавливаем того, кто проводит изменение данных, и возвращаем ответ дальше."""
        response = super().form_valid(form)
        if form.is_valid():
            form.instance.updated_by = User.objects.get(pk=self.request.user.pk)
            return response

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном изменении лида, перенаправляет на страницу с деталями этого лида."""

        return reverse_lazy("leads:leads_detail", kwargs={"pk": self.object.pk})


class LeadDeleteView(DeleteView):
    model = Lead
    context_object_name = "lead"

    def get_success_url(self) -> HttpResponseRedirect:
        messages.success(
            self.request,
            f"Удаление {self.model.__name__}: {self.object.full_name!r}, прошло успешно!",
        )
        return reverse_lazy("leads:leads_list")


@transaction.atomic
def convert_lead_to_customer(request, *args, **kwargs):
    lead_id = kwargs.get("lead_id")
    lead = get_object_or_404(Lead, pk=lead_id)

    customer, created = Customer.objects.get_or_create(
        lead=lead,
        defaults={
            "created_by": request.user,
            "updated_by": request.user,
            "archived": False,
        },
    )

    if not created:
        customer.archived = False
        customer.save()

    lead.is_active = True
    lead.save()

    return redirect("leads:leads_list")


@transaction.atomic
def convert_lead_to_inactive(request, *args, **kwargs):
    lead_id = kwargs.get("lead_id")
    lead = get_object_or_404(Lead, pk=lead_id)

    customer = get_object_or_404(Customer, lead=lead)
    customer.updated_by = request.user
    customer.archived = True
    customer.save()

    lead.is_active = False
    lead.save()

    return redirect("leads:leads_list")
