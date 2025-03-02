from django.urls import path

from .views import CustomerListView, CustomerCreateView, CustomerDetailView


app_name = "customers"

urlpatterns = [
    path("", CustomerListView.as_view(), name="customers_list"),
    path("new/", CustomerCreateView.as_view(), name="customers_create"),
    path("<int:pk>/", CustomerDetailView.as_view(), name="customers_detail"),
]
