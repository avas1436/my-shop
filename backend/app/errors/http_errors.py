from fastapi import HTTPException

from app.errors.errors import HttpError, InternalServerError, ServiceError


def to_http_exception(err: HttpError) -> HTTPException:
    return HTTPException(
        status_code=err.status_code,
        detail={
            "message": err.message,
            "code": err.code,
            "details": err.details,
        },
    )


def map_service_error(e: ServiceError) -> HttpError:
    """
    Convert domain errors to HttpError.
    Customize per your project.
    """

    return InternalServerError(message=str(e))
