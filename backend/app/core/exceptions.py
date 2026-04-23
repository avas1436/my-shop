from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


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

    @app.middleware("http")
    async def catch_exceptions(request: Request, call_next):

        try:
            return await call_next(request)

        except Exception as e:
            logger.error(
                f"Unhandled Exception: {e} - Path: {request.url}",
                exc_info=True,  # شامل traceback
            )
            return JSONResponse(
                status_code=500,
                content=error_payload(
                    status_code=500,
                    detail="Internal server error",
                    error_type="ServerError",
                    request=request,
                ),
            )
