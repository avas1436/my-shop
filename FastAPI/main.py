from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import app.models
from app.api.v1.router import api_router
from app.config.cors import setup_cors
from app.config.logging_config import setup_logger
from app.config.settings import get_settings
from app.core.database import engine
from app.core.exceptions import register_exception_handlers
from app.core.redis import RedisController


# -------------------------------------------------------------
# Lifespan
# -------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):

    # -------------------------------------------------------------
    # Settings
    # -------------------------------------------------------------
    settings = get_settings()
    app.state.settings = settings

    # -------------------------------------------------------------
    # Logger
    # -------------------------------------------------------------
    logger = setup_logger(level=settings.log_level)
    app.state.logger = logger

    logger.info("App starting...")

    # -----------------------------
    # Database
    # -----------------------------
    app.state.db_engine = engine

    # -------------------------------------------------------------
    # Redis
    # -------------------------------------------------------------
    redis_controller = RedisController(
        redis_url=settings.redis_url,
        redis_max_connections=settings.redis_max_connections,
        redis_socket_timeout=settings.redis_socket_timeout,
        session_prefix=settings.session_prefix,
    )

    try:
        await redis_controller.init_redis()
        logger.info("Redis initialized")
    except Exception as e:
        logger.error(f"Redis initialization failed: {e}")
        redis_controller = None

    app.state.redis = redis_controller

    yield

    if redis_controller:
        logger.info("Closing Redis...")
        await redis_controller.close_redis()
        logger.info("Redis closed")

    logger.info("App shutting down...")


# -------------------------------------------------------------
# App Factory
# -------------------------------------------------------------
def create_app() -> FastAPI:
    settings = get_settings()
    logger = setup_logger(level=settings.log_level)

    # -------------------------------------------------------------
    # Create App instance
    # -------------------------------------------------------------
    # app = FastAPIOffline(
    #     title=settings.app_name,
    #     version=settings.app_version,
    #     debug=settings.debug,
    #     openapi_url=settings.openapi_url,
    #     docs_url=settings.docs_url,
    #     redoc_url=settings.redoc_url,
    #     lifespan=lifespan,
    # )
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        # کنترل مستندات از طریق پارامترهای استاندارد
        openapi_url=settings.openapi_url if settings.docs_enable else None,
        docs_url=settings.docs_url if settings.docs_enable else None,
        redoc_url=settings.redoc_url if settings.docs_enable else None,
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

    # -------------------------------------------------------------
    # Routes
    # -------------------------------------------------------------
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    # -------------------------------------------------------------
    # Media route for local images
    # -------------------------------------------------------------
    app.mount(
        "/media",
        StaticFiles(directory=settings.media_root),
        name="media",
    )

    # -------------------------------------------------------------
    # MiddleWares
    # -------------------------------------------------------------
    # register_middlewares(app=app, trusted_host=settings.trusted_hosts)

    # -------------------------------------------------------------
    # Exception Handlers
    # -------------------------------------------------------------
    register_exception_handlers(app=app, logger=logger)

    # -------------------------------------------------------------
    # Check health
    # -------------------------------------------------------------
    @app.get("/health")
    async def healthcheck() -> dict[str, str]:
        return {
            "Status": "ok",
            "Environment": settings.env,
            "App": settings.app_name,
            "App version": settings.app_version,
            "Debug": str(settings.debug),
            "Log Level": settings.log_level,
            "Time Zone": settings.timezone,
        }

    return app


# -------------------------------------------------------------
# App
# -------------------------------------------------------------
app = create_app()


# آموزش استفاده از تنظیمات، لاگر و ردیس در بقیه پروژه:

# در یک روت:
# @app.get("/config")
# async def config(request: Request):
#     settings = request.app.state.settings
#     return {"mode": settings.MODE}

# در یک دیپندنسی :
# def get_settings(request: Request):
#     return request.app.state.settings
