from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ads.models import AdsCompany
from customers.models import Customer
from leads.models import Lead
from service_product.models import Product


def general_statistics(request: HttpRequest) -> HttpResponse:
    """Представление для главной страницы, с информацией об общей статистикой."""
    home_page = "crm_service/index.html"
    products_count = Product.objects.all().count()
    advertisements_count = AdsCompany.objects.all().count()
    leads_count = Lead.objects.all().count()
    customers_count = Customer.objects.all().count()
    context = {
        "products_count": products_count,
        "advertisements_count": advertisements_count,
        "leads_count": leads_count,
        "customers_count": customers_count,
    }
    return render(request=request, template_name=home_page, context=context)
