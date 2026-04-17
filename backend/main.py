from contextlib import asynccontextmanager
from fastapi_offline import FastAPIOffline
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.config.cors import setup_cors
from app.config.logging_config import setup_logger
from app.config.settings import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.middlewares import register_middlewares
from app.core.redis import RedisController
from app.core.database import engine
from app.migrations.env import run_migrations


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

    # -----------------------------
    # Run migrations
    # -----------------------------
    try:
        logger.info("Running Alembic migrations...")
        await run_migrations()
        logger.info("Migrations applied successfully.")
    except Exception as e:
        logger.error(f"Migration error: {e}")
        raise

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
    logger = setup_logger()

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

    # -------------------------------------------------------------
    # MiddleWares
    # -------------------------------------------------------------
    register_middlewares(app=app, trusted_host=settings.trusted_hosts)

    # -------------------------------------------------------------
    # Exception Handlers
    # -------------------------------------------------------------
    register_exception_handlers(app=app, logger=logger)

    # -------------------------------------------------------------
    # Routes
    # -------------------------------------------------------------
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    # -------------------------------------------------------------
    # Check health
    # -------------------------------------------------------------
    @app.get("/health", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok", "app": settings.app_name}

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
