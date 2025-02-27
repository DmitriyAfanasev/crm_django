from django.urls import path

from .views import AdsCompanyListView, AdsCompanyCreateView

app_name: str = "ads"

urlpatterns: list[path] = [
    path("", AdsCompanyListView.as_view(), name="ads_list"),
    path("new/", AdsCompanyCreateView.as_view(), name="ads_create"),
]
