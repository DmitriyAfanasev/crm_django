from django.urls import path

from .api import api

appname = "api"

urlpatterns = [path("", api.urls),]