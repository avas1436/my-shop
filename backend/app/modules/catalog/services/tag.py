import math

from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.redis_cache import RedisCache
from app.common.pagination import PageMeta, PageResponse
from app.core.utils import slugify
from app.modules.catalog.models.tag import Tag
from app.modules.catalog.repository.tag import TagRepository
from app.modules.catalog.schemas.tag import TagCreate, TagRead, TagUpdate


class TagService:
    def __init__(self, db: AsyncSession, request: Request):
        self.repo = TagRepository(db)
        self.cache = RedisCache(request)

    # -------------------------
    # create a tag
    # -------------------------
    async def create_tag(self, data: TagCreate) -> Tag:

        if await self.repo.get_by_name(data.name):
            raise HTTPException(status_code=409, detail="Tag name already exists.")

        slug = data.slug or slugify(data.name)
        if slug and await self.repo.get_by_slug(slug):
            raise HTTPException(status_code=409, detail="Tag slug already exists.")

        tag = Tag(name=data.name, slug=slug)
        tag = await self.repo.create(tag)

        if self.cache.is_available():
            await self.cache.invalidate_lists()

        return tag

    # -------------------------
    # get a tag
    # -------------------------
    async def get_tag(self, tag_id: int) -> dict:
        if self.cache.is_available():
            cached = await self.cache.get("tag", tag_id)
            if cached is not None:
                return cached

        tag = await self.repo.get_by_id(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found.")

        payload = TagRead.model_validate(tag).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set("tag", tag_id, payload=payload)

        return payload

    # -------------------------
    # list tags
    # -------------------------
    async def list_tags(
        self,
        search: str | None,
        tag_id: int | None,
        page: int,
        size: int,
    ) -> PageResponse[dict]:

        if page < 1 or size < 1 or size > 100:
            raise HTTPException(status_code=400, detail="Invalid pagination values.")

        if self.cache.is_available():
            cached = await self.cache.get_list(
                "list",
                "tag",
                search,
                tag_id,
                page,
                size,
            )
            if cached is not None:
                return PageResponse(**cached)

        items, total = await self.repo.list_filtered(search, tag_id, page, size)

        pages = math.ceil(total / size) if total else 1
        response_items = []
        for t in items:
            response_items.append(
                {
                    "id": t.id,
                    "name": t.name,
                    "slug": t.slug,
                    "created_at": t.created_at,
                }
            )

        resp = PageResponse(
            items=response_items,
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

        if self.cache.is_available():
            await self.cache.set_list(
                "list",
                "tag",
                search,
                tag_id,
                page,
                size,
                payload=resp.model_dump(mode="json"),
            )

        return resp

    # -------------------------
    # update a tag
    # -------------------------
    async def update_tag(self, tag_id: int, data: TagUpdate) -> Tag:
        tag = await self.repo.get_by_id(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found.")

        if data.name and data.name != tag.name:
            if await self.repo.get_by_name(data.name):
                raise HTTPException(status_code=409, detail="Tag name already exists.")
            tag.name = data.name

        if data.slug:
            if data.slug != tag.slug and await self.repo.get_by_slug(data.slug):
                raise HTTPException(status_code=409, detail="Tag slug already exists.")
            tag.slug = data.slug

        tag = await self.repo.update(tag)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("tag", tag_id)

        return tag

    # -------------------------
    # delete a tag
    # -------------------------
    async def delete_tag(self, tag_id: int) -> None:
        tag = await self.repo.get_by_id(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found.")

        await self.repo.delete(tag)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("tag", tag_id)
