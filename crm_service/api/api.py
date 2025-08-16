from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.responses import Response


from api.routers.product_router import router as product_router
from api.schemas.ads_schemas import (
    AdsCompanyResponseSchema1,
    AdsCompanyCreateSchemaModel,
    AdsCompanyResponseSchema,
)
from ads.models import AdsCompany

if TYPE_CHECKING:
    from django.http import HttpRequest

api = NinjaAPI()
api.add_router(router=product_router, prefix="/products")


@api.get("/company_schema")
def get_comp_schema(request: "HttpRequest", comp_id: int):
    mod = get_object_or_404(AdsCompany, id=comp_id)
    res = AdsCompanyResponseSchema.model_validate(mod)
    return res


@api.get(
    "/company_model",
)
def get_comp_model(
    request: "HttpRequest", comp_id: int
) -> AdsCompanyResponseSchema1:
    if company_orm := get_object_or_404(AdsCompany, id=comp_id):
        return AdsCompanyResponseSchema1.model_validate(company_orm)


@api.post("/company")
def post_comp_schema(
    request: "HttpRequest",
    schema: AdsCompanyCreateSchemaModel,
) -> Response:
    if AdsCompany.objects.filter(name=schema.name).exists():
        return 400, {"error": "This name already exists"}
    company = AdsCompany.objects.create(
        name=schema.name,
        product_id=schema.product_id,
        channel_id=schema.channel_id,
        budget=schema.budget,
        country=schema.country,
        email=schema.email,
        website=schema.website,
    )
    return 201, f"{company.name} created"
