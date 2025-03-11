from django.urls import path

from .views import (
    LeadListView,
    LeadCreateView,
    LeadDetailView,
    LeadUpdateView,
    LeadDeleteView,
    # convert_lead_to_customer,
    # convert_lead_to_inactive,
)

app_name = "leads"

urlpatterns = [
    path("", LeadListView.as_view(), name="leads_list"),
    path("new/", LeadCreateView.as_view(), name="leads_create"),
    path("<int:pk>/", LeadDetailView.as_view(), name="leads_detail"),
    path("<int:pk>/edit/", LeadUpdateView.as_view(), name="leads_edit"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="leads_delete"),
    # path(
    #     "new_active/<int:lead_id>/",
    #     convert_lead_to_customer,
    #     name="convert_lead_to_customer",
    # ),
    # path(
    #     "inactive/<int:lead_id>/",
    #     convert_lead_to_inactive,
    #     name="convert_lead_to_inactive",
    # ),
]
