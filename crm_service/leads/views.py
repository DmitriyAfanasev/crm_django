from django.contrib import messages
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
