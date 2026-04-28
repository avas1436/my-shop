from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import PageResponse

# from redis.asyncio import Redis
from app.core.database import get_db

# from app.cache.controller import get_redis_client
from app.modules.catalog.schemas.brand import BrandCreate, BrandRead, BrandUpdate
from app.modules.catalog.services.brand import BrandService

router = APIRouter()


@router.post("/", response_model=BrandRead)
async def create_brand(
    data: BrandCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
):
    return await BrandService(db=db, request=request).create_brand(data)


@router.get("/{brand_id}", response_model=BrandRead)
async def get_brand(
    brand_id: int,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    base_url = str(request.base_url)
    return await BrandService(db=db, request=request).get_brand(brand_id, base_url)


@router.get("/", response_model=PageResponse[dict])
async def list_brands(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    search: str | None = None,
    brand_id: int | None = None,
    page: int = 1,
    size: int = 10,
):
    base_url = str(request.base_url)
    return await BrandService(db=db, request=request).list_brands(
        search, brand_id, page, size, base_url
    )


@router.put("/{brand_id}", response_model=BrandRead)
async def update_brand(
    brand_id: int,
    data: BrandUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
):
    return await BrandService(db=db, request=request).update_brand(brand_id, data)


@router.delete("/{brand_id}")
async def delete_brand(
    brand_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
):
    await BrandService(db=db, request=request).delete_brand(brand_id)
    return {"detail": "Brand deleted successfully."}
