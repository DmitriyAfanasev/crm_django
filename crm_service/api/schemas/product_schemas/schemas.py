from ninja import ModelSchema

from service_product.models import Product


class ProductSchema(ModelSchema):
    class Meta:
        model = Product
        fields = "__all__"
