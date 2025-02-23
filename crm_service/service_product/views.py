from django.core.paginator import Paginator
from django.views.generic import ListView

from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "service_product/products-list.html"
    paginator_class = Paginator
    paginate_by = 5
