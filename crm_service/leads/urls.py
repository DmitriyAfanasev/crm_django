from django.urls import path

from .views import (
    LeadListView,
    LeadCreateView,
    LeadDetailView,
    LeadUpdateView,
    LeadDeleteView,
)

app_name = "leads"

urlpatterns = [
    path("", LeadListView.as_view(), name="leads_list"),
    path("new/", LeadCreateView.as_view(), name="leads_create"),
    path("<int:pk>/", LeadDetailView.as_view(), name="leads_detail"),
    path("<int:pk>/edit/", LeadUpdateView.as_view(), name="leads_edit"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="leads_delete"),
]
