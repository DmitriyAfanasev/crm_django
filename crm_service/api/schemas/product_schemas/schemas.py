from typing import Optional, Annotated

from ninja import Field, ModelSchema, Schema
from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt

from service_product.models import Product

type NotNegativeLenStr = Annotated[str, Field(min_length=1, max_length=255)]


class CategorySchema(Schema):
    title: NotNegativeLenStr
    description: NotNegativeLenStr


class ProductFilter(Schema):
    search: str = Field(
        ...,
        description="### Search by input text"
    )


class PaginationFilter(Schema):
    limit: PositiveInt = 20
    offset: NonNegativeInt = 0


class ProductSchema(ModelSchema):
    # category: CategorySchema

    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ["category"]

class CreateProductSchema(ModelSchema):
    created_by: int = Field(..., description="User ID of the creator")

    class Meta:
        model = Product
        exclude = [
            "id",
            "created_at",
            "updated_at",
            "archived",
            "updated_by",
        ]


class UpdateProductSchema(Schema):
    name: Optional[str] = Field(..., description="Product name")
    description: Optional[str] = Field(..., description="Product description")
    cost: Optional[NonNegativeFloat] = Field(..., description="Product cost")
    discount: Optional[NonNegativeInt] = Field(..., description="Product discount")
    status: Optional[str] = Field(..., description="Product status")
