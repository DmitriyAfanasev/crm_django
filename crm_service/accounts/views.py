from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    template_name: str = "accounts/login.html"
    success_url: str = reverse_lazy("home")


class MyLogoutView(LogoutView):
    template_name: str = "accounts/logout.html"
    next_page: str = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if request.user.is_authenticated:
            logout(request)
        return redirect(reverse_lazy("accounts:login"))
