from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "crm_service/_base.html"
