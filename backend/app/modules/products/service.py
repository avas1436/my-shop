from app.cache.product_cache import ProductCache
from app.core.utils import slugify
from app.modules.products.models import Product
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import ProductCreate


class ProductService:
    def __init__(self, repository: ProductRepository, cache: ProductCache | None = None):
        self.repository = repository
        self.cache = cache

    async def create(self, payload: ProductCreate) -> Product:
        product = Product(
            name=payload.name,
            slug=slugify(payload.name),
            description=payload.description,
            price=payload.price,
            category_id=payload.category_id,
        )
        created = await self.repository.create(product)
        if self.cache:
            await self.cache.set_product(created.id, {
                "id": created.id,
                "name": created.name,
                "price": created.price,
            })
        return created

    async def list_all(self) -> list[Product]:
        return await self.repository.list_all()

    async def get_by_id(self, product_id: int) -> Product | dict | None:
        if self.cache:
            cached = await self.cache.get_product(product_id)
            if cached:
                return cached
        return await self.repository.get_by_id(product_id)
