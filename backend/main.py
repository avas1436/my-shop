from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config.cors import setup_cors
from app.config.logging_config import setup_logging
from app.config.settings import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.middlewares import register_middlewares


settings = get_settings()
setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

setup_cors(app)
register_middlewares(app)
register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}
