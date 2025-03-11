"""
URL configuration for crm_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from .views import general_statistics


# TODO добавить i18n_patterns
urlpatterns = [
    path("", general_statistics, name="home"),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("products/", include("service_product.urls")),
    path("ads/", include("ads.urls")),
    path("leads/", include("leads.urls")),
    path("customers/", include("customers.urls")),
    path("contracts/", include("contracts.urls")),
    # path("reg/", include("django.contrib.auth.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
