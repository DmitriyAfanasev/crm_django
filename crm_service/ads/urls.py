from django.urls import path

from .views import AdsCompanyListView, AdsCompanyCreateView, AdsCompanyDetailView

app_name: str = "ads"

urlpatterns: list[path] = [
    path("", AdsCompanyListView.as_view(), name="ads_list"),
    path("new/", AdsCompanyCreateView.as_view(), name="ads_create"),
    path("<int:pk>/", AdsCompanyDetailView.as_view(), name="ads_detail"),
]
