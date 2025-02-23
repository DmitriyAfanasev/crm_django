from django.urls import path

from .views import ProductListView

app_name = "service_product"
urlpatterns = [
    path("", ProductListView.as_view(), name="service_list"),
]
