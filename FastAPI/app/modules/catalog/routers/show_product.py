# app/modules/catalog/routers/show_product.py
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status

from app.common.enums import ProductSortEnum
from app.common.pagination import PageResponse
from app.common.responses import SuccessAPIRoute
from app.core.middlewares import limiter
from app.modules.catalog.dependencies.product import get_user_product_service
from app.modules.catalog.schemas.product import (
    ProductFullUserRead,
    ProductUserLightRead,
)
from app.modules.catalog.services.product import UserProductService

router = APIRouter(route_class=SuccessAPIRoute)


# =========================================================
# 1) Homepage - Featured Products
# =========================================================
@router.get(
    "/home",
    response_model=list[ProductUserLightRead],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute; 1000/day")
async def homepage_featured_products(
    request: Request,
    service: Annotated[UserProductService, Depends(get_user_product_service)],
    limit: int = Query(12, ge=1, le=50),
):
    return await service.get_homepage(limit=limit)


# =========================================================
# 2) Search Products (paginated)
# =========================================================
@router.get(
    "/search",
    response_model=PageResponse[dict],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("20/minute; 300/hour")
async def search_products(
    request: Request,
    service: Annotated[UserProductService, Depends(get_user_product_service)],
    q: Annotated[str | None, Query(min_length=1, max_length=200)] = None,
    brand_slugs: Annotated[list[str] | None, Query()] = None,
    category_slugs: Annotated[list[str] | None, Query()] = None,
    tag_slugs: Annotated[list[str] | None, Query()] = None,
    min_price: Annotated[int | None, Query(ge=0)] = None,
    max_price: Annotated[int | None, Query(ge=0)] = None,
    is_in_stock: Annotated[bool | None, Query()] = None,
    has_discount: Annotated[bool | None, Query()] = None,
    is_featured: Annotated[bool | None, Query()] = None,
    is_digital: Annotated[bool | None, Query()] = None,
    sort: Annotated[ProductSortEnum | None, Query()] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return await service.search_products(
        q=q,
        brand_slugs=brand_slugs,
        category_slugs=category_slugs,
        tag_slugs=tag_slugs,
        attribute_filters=None,
        min_price=min_price,
        max_price=max_price,
        is_in_stock=is_in_stock,
        has_discount=has_discount,
        is_featured=is_featured,
        is_digital=is_digital,
        sort=sort,
        page=page,
        size=size,
    )


# =========================================================
# 3) Full Product by ID
# =========================================================
@router.get(
    "/{product_id}",
    response_model=ProductFullUserRead,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute; 1000/day")
async def get_product_by_id(
    request: Request,
    product_id: int,
    service: Annotated[UserProductService, Depends(get_user_product_service)],
):
    return await service.get_product_detail(product_id=product_id)


# =========================================================
# 4) Full Product by Slug
# =========================================================
@router.get(
    "/slug/{slug}",
    response_model=ProductFullUserRead,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute; 1000/day")
async def get_product_by_slug(
    request: Request,
    slug: str,
    service: Annotated[UserProductService, Depends(get_user_product_service)],
):
    return await service.get_product_detail(slug=slug)
