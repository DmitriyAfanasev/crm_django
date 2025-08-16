from ninja import Schema, ModelSchema


from ads.models import AdsCompany
from ads.models_as_description.promotion_channels import PromotionChannel

from api.schemas.product_schemas import ProductSchema


class PromotionChannelSchema(ModelSchema):
    class Meta:
        model = PromotionChannel
        fields = "__all__"


class AdsCompanyResponseSchema1(Schema):
    id: int
    name: str
    product: ProductSchema
    channel: PromotionChannelSchema
    budget: float
    country: str
    email: str
    website: str

    class Config:
        orm_mode = True


class AdsCompanyResponseSchema(Schema):
    """Schema for AdsCompany"""

    id: int
    name: str
    product: ProductSchema
    channel: PromotionChannelSchema
    budget: float
    country: str
    email: str
    website: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            "description": "AdsCompany response schema сука",
            "example": {
                "id": 123123,
                "product": {
                    "id": 12,
                    "name": "product name",
                    "description": "product description",
                    "cost": 123000000,
                    "discount": 5,
                    "status": "active",
                    "archived": False,
                },
                "budget": 100000000000000000,
                "country": "US",
                "email": "asd@asd.com",
                "website": "https://website.com",
            },
            "media_type": {
                "type": "object",
            },
        }


class AdsCompanyCreateSchemaModel(ModelSchema):
    class Meta:
        model = AdsCompany
        fields = "__all__"
        exclude = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
