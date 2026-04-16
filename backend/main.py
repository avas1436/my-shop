from contextlib import asynccontextmanager
from fastapi_offline import FastAPIOffline
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.config.cors import setup_cors
from app.config.logging_config import setup_logger
from app.config.settings import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.middlewares import register_middlewares


# -------------------------------------------------------------
# Settings
# -------------------------------------------------------------
settings = get_settings()


# -------------------------------------------------------------
# Logger
# -------------------------------------------------------------
logger = setup_logger(level=settings.log_level)


# -------------------------------------------------------------
# Lifespan
# -------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting...")

    yield

    print("App shouting down...")


# -------------------------------------------------------------
# Create App instance
# -------------------------------------------------------------
app = FastAPIOffline(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    openapi_url=settings.openapi_url,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    lifespan=lifespan,
)

# -------------------------------------------------------------
# CORS
# -------------------------------------------------------------
setup_cors(
    app=app,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
    expose_headers=settings.cors_expose_headers,
    max_age=settings.cors_max_age,
)


register_middlewares(app)

# -------------------------------------------------------------
# Exception Handlers
# -------------------------------------------------------------
register_exception_handlers(app=app, logger=logger)


app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}
