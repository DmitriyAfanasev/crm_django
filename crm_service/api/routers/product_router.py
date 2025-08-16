import datetime
from typing import TYPE_CHECKING

from django.db import connection
from django.db.models import F, Q, FloatField
from django.db.models.functions import Cast, Greatest
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
)
from ninja import Router, Query
from ninja.responses import Response

from api.schemas.product_schemas import (
    ProductSchema,
    CreateProductSchema,
    UpdateProductSchema,
    ProductFilter,
    PaginationFilter,
)
from api.schemas.common_schemas import ApiResponse
from api.schemas.product_schemas.schemas import CategorySchema

from service_product.models import Product, Category
from utils.keyboard import switch_layout
from django.db import connection

if TYPE_CHECKING:
    from django.http import HttpRequest

router = Router(tags=["Products"])

User = get_user_model()


@router.get("/id", summary="самари", response=ApiResponse[ProductSchema])
def get_product_by_id(
    request: "HttpRequest",
    product_id: int,
) -> ApiResponse[ProductSchema]:
    """### Некоторое описание с md форматом!"""
    try:
        product = Product.objects.get(id=product_id)
        return ProductSchema.from_orm(product)
    except Product.DoesNotExist as error:
        return Response({"error": str(error)}, status=404)


@router.get("/")
def get_products_list(request: "HttpRequest"):
    products = [
        ProductSchema.from_orm(product)
        for product in Product.objects.filter(archived=False).order_by("-id")
    ]
    return {"count": len(products), "page": 1, "products": products}


@router.post("/")
def create_product(
    request: "HttpRequest", product: CreateProductSchema
) -> ProductSchema:
    product_data = CreateProductSchema.model_validate(product)
    product: Product = Product.objects.create(
        created_by_id=product_data.created_by,
        name=product_data.name,
        description=product_data.description,
        cost=product_data.cost,
        discount=product_data.discount,
        status=product_data.status,
    )

    return ProductSchema.from_orm(product)


@router.patch("/")
def update_product(
    request: "HttpRequest",
    update_data: UpdateProductSchema,
    product_id: int,
) -> ProductSchema:
    try:
        if Product.objects.get(pk=product_id):
            updated_product = Product.objects.filter(pk=product_id).update(
                **update_data.dict()
            )
        return ProductSchema.from_orm(updated_product)
    except Product.DoesNotExist as error:
        return Response({"error": str(error)}, status=404)


@router.get("/search")
def search_data_by_products(
    request: "HttpRequest",
    filters: Query[ProductFilter],
) -> list[ProductSchema]:
    """## Поиск данных среди услуг по названию и описанию."""
    product_list = Product.objects.filter(
        Q(name__icontains=filters.search) | Q(description__icontains=filters.search)
    )
    return [ProductSchema.from_orm(product) for product in product_list]


@router.get("/search_cheap_service")
def search_cheap_service(
    request: "HttpRequest",
    filters: Query[ProductFilter],
    pagination: Query[PaginationFilter],
) -> list[ProductSchema]:
    """Поиск услуг, которые дешевле указанной цены."""
    qs = Product.objects.filter(archived=False)

    if filters.search is not None:
        qs = qs.filter(cost__lt=filters.search)

    qs = qs.order_by("-cost", "id")

    start = pagination.offset
    limit = pagination.limit
    qs = qs[start : start + limit]
    all_availability = (
        len([prod for prod in Product.objects.filter(archived=False)]) - start - limit
    )
    if all_availability <= 0:
        all_availability = "В базе больше нет доступных услуг."

    return {
        "result": [ProductSchema.from_orm(p) for p in qs],
        "search": filters.search,
        "limit": limit,
        "offset": start,
        "Сколько_ещё_доступно": all_availability,
    }


@router.get("/last_products_by_last_10_days", response=list[ProductSchema])
def get_services_by_last_10_days(
    request: "HttpRequest",
    pagination: Query[PaginationFilter],
) -> list[ProductSchema]:
    today = datetime.date.today()
    product_list = Product.objects.filter(created_at__lte=today).order_by(
        "-created_at"
    )[pagination.offset : pagination.limit]
    return [ProductSchema.from_orm(product) for product in product_list]


@router.get("get_by_category", response=list[ProductSchema])
def get_services_by_category(
    request: "HttpRequest",
    filters: Query[ProductFilter],
    pagination: Query[PaginationFilter],
) -> list[ProductSchema]:
    product_list = Product.objects.filter(
        category__title__icontains=filters.search
    ).order_by("-created_at")[pagination.offset : pagination.limit]
    return [ProductSchema.from_orm(product) for product in product_list]


@router.get("get_full_text", response=list[ProductSchema])
def get_by_text(
    request: "HttpRequest",
    filters: Query[ProductFilter],
    pagination: Query[PaginationFilter],
) -> list[ProductSchema]:
    term = filters.search
    vector = SearchVector("name", weight="A", config="russian") + SearchVector(
        "description", weight="B", config="russian"
    )
    query = SearchQuery(term, config="russian")

    qs = (
        Product.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank", "id")[pagination.offset : pagination.limit]
    )
    return [ProductSchema.from_orm(p) for p in qs[:50]]


@router.get("/matching_search")
def get_by_matching(
    request: "HttpRequest",
    search_term: str,
    pagination: Query[PaginationFilter],
    min_similarity: float = 0.3,
) -> list[ProductSchema]:
    """
    Поиск по триграммной схожести

    Параметры:
    - search_term: искомый текст
    - min_similarity: минимальный порог схожести (0.0-1.0)
    - pagination: параметры пагинации

    Возвращает продукты, где имя ИЛИ описание похожи на search_term
    """
    # Находим продукты
    products = (
        Product.objects.annotate(
            name_similarity=TrigramSimilarity("name", search_term),
            desc_similarity=TrigramSimilarity("description", search_term),
        )
        .filter(
            Q(name_similarity__gte=min_similarity)
            | Q(desc_similarity__gte=min_similarity)
        )
        .select_related("category")[  # загружаем категории чтоб убрать N+1
            pagination.offset : pagination.limit
        ]
    )

    # Группируем по категориям
    categories = {}
    for product in products:
        category_name = product.category.title
        if category_name not in categories:
            categories[category_name] = {"products": [], "count": 0}
        categories[category_name]["products"].append(ProductSchema.from_orm(product))
        categories[category_name]["count"] += 1

    result = [
        {"category_name": name, "products": data["products"], "count": data["count"]}
        for name, data in categories.items()
    ]

    return {"result": result}


@router.get("/search_if_there_is_an_error_in_the_keyboard_layout")
def search_if_there_is_an_error_in_the_keyboard_layout(
    request: "HttpRequest",
    search_term: str,
    pagination: Query[PaginationFilter],
    min_similarity: float = 0.25,
):
    # 1) варианты запроса (как есть, en->ru, ru->en)
    v0, v_en2ru, v_ru2en = switch_layout(search_term)
    variants = [x for x in {v0, v_en2ru, v_ru2en} if x]
    if not variants:
        return {"result": [], "variants": []}

    qs = Product.objects.filter(archived=False)

    # 2) Для КАЖДОГО варианта добавляем аннотацию с уникальным именем
    sim_aliases = []
    for idx, v in enumerate(variants):
        alias = f"sim_{idx}"
        sim_expr = TrigramSimilarity("name", v) + TrigramSimilarity("description", v)
        qs = qs.annotate(**{alias: sim_expr})
        sim_aliases.append(alias)

    # 3) Фильтр: (sim_0>=thr) OR (sim_1>=thr) ...
    cond = Q()
    for alias in sim_aliases:
        cond |= Q(**{f"{alias}__gte": min_similarity})
    qs = qs.filter(cond)

    # 4) Лучшая схожесть для сортировки
    if len(sim_aliases) == 1:
        qs = qs.annotate(best_sim=F(sim_aliases[0]))
    else:
        qs = qs.annotate(best_sim=Greatest(*(F(a) for a in sim_aliases)))

    qs = qs.order_by("-best_sim", "-id")
    # 5) Пагинация
    start = pagination.offset or 0
    limit = pagination.limit or 20
    page = qs[start : start + limit]
    products = [ProductSchema.from_orm(p) for p in page]

    return {
        "query": search_term,
        "variants": variants,
        "result": products,
        "count_connection": f"кол-во запросов к базе - {len(connection.queries)}",
    }
