from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.errors.errors import HttpError, InternalServerError, ServiceError
from app.errors.http_errors import map_service_error, to_http_exception


def error_payload(status_code: int, detail, error_type: str, request: Request):
    return {
        "success": False,
        "status_code": status_code,
        "error_type": error_type,
        "detail": detail,
        "path": request.url.path,
        "timestamp": datetime.now(UTC).isoformat(),
    }


def register_exception_handlers(app: FastAPI, logger) -> None:

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):

        logger.warning(f"HTTPException: {exc.detail} - Path: {request.url}")

        return JSONResponse(
            status_code=exc.status_code,
            content=error_payload(
                status_code=exc.status_code,
                detail=exc.detail,
                error_type="HTTPException",
                request=request,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):

        logger.warning(f"ValidationError: {exc.errors()} - Path: {request.url}")

        return JSONResponse(
            status_code=422,
            content=error_payload(
                status_code=422,
                detail=exc.errors(),
                error_type="RequestValidationError",
                request=request,
            ),
        )

    @app.exception_handler(HttpError)
    async def http_error_handler(request: Request, exc: HttpError):
        logger.warning(f"HttpError: {exc.message} - Path: {request.url}")
        http_exc = to_http_exception(exc)
        return JSONResponse(
            status_code=http_exc.status_code,
            content=error_payload(
                status_code=http_exc.status_code,
                detail=http_exc.detail,
                error_type=exc.__class__.__name__,
                request=request,
            ),
        )

    @app.exception_handler(ServiceError)
    async def service_error_handler(request: Request, exc: ServiceError):
        logger.warning(f"ServiceError: {exc} - Path: {request.url}")
        http_err = map_service_error(exc)
        http_exc = to_http_exception(http_err)
        return JSONResponse(
            status_code=http_exc.status_code,
            content=error_payload(
                status_code=http_exc.status_code,
                detail=http_exc.detail,
                error_type=exc.__class__.__name__,
                request=request,
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Exception: {exc} - Path: {request.url}", exc_info=True)
        http_err = InternalServerError(message="Internal server error")
        http_exc = to_http_exception(http_err)
        return JSONResponse(
            status_code=http_exc.status_code,
            content=error_payload(
                status_code=http_exc.status_code,
                detail=http_exc.detail,
                error_type="ServerError",
                request=request,
            ),
        )
