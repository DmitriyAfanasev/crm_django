from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    """
    Кастомное представление для авторизации пользователя.

    Атрибуты:
        template_name (str): Путь к шаблону страницы авторизации.
        success_url (str): URL для перенаправления после успешной авторизации.
    """

    template_name: str = "accounts/login.html"
    success_url: str = reverse_lazy("home")


class MyLogoutView(LogoutView):
    """
    Кастомное представление для выхода пользователя из системы.

    Атрибуты:
        template_name (str): Путь к шаблону страницы выхода.
        next_page (str): URL для перенаправления после выхода.
    """

    template_name: str = "accounts/logout.html"
    next_page: str = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """
        Обрабатывает запрос на выход пользователя.

        Если пользователь авторизован, выполняется выход из системы
        и перенаправление на страницу авторизации.
        """
        if request.user.is_authenticated:
            logout(request)
        return redirect(reverse_lazy("accounts:login"))
