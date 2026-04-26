from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db_session
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import ProductCreate, ProductRead
from app.modules.products.service import ProductService

router = APIRouter()


@router.get("/", response_model=list[ProductRead])
async def list_products(
    db: AsyncSession = Depends(get_db_session),
) -> list[ProductRead]:
    service = ProductService(ProductRepository(db))
    products = await service.list_all()
    return [ProductRead.model_validate(product) for product in products]


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreate, db: AsyncSession = Depends(get_db_session)
) -> ProductRead:
    service = ProductService(ProductRepository(db))
    product = await service.create(payload)
    return ProductRead.model_validate(product)
