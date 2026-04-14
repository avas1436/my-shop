from app.core.utils import slugify
from app.modules.categories.models import Category
from app.modules.categories.repository import CategoryRepository
from app.modules.categories.schemas import CategoryCreate


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def create(self, payload: CategoryCreate) -> Category:
        category = Category(name=payload.name, slug=slugify(payload.name))
        return await self.repository.create(category)

    async def list_all(self) -> list[Category]:
        return await self.repository.list_all()
