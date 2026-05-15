from typing import Any


class ServiceError(Exception):
    """Base error for business/service layer (domain error)."""

    pass


class HttpError(Exception):
    """
    Base HTTP error.
    Use this when you want to raise HTTP-like errors in service layer
    (or manually in routers).
    """

    status_code: int = 500

    def __init__(
        self,
        message: str | None = None,
        *,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message or self.__class__.__name__)
        self.message = message or self.__class__.__name__
        self.code = code
        self.details = details


# =========================
# 4xx Client Errors
# =========================


class BadRequest(HttpError):
    """400: when request data is invalid/incorrect (validation failure, malformed input)."""

    status_code = 400


class Unauthorized(HttpError):
    """401: when authentication is missing or invalid (no token, invalid token)."""

    status_code = 401


class PaymentRequired(HttpError):
    """402: reserved for future use (rare; paywall/billing scenarios)."""

    status_code = 402


class Forbidden(HttpError):
    """403: user is authenticated but lacks permission for this action."""

    status_code = 403


class NotFound(HttpError):
    """404: resource does not exist."""

    status_code = 404


class MethodNotAllowed(HttpError):
    """405: HTTP method not allowed on this endpoint."""

    status_code = 405


class NotAcceptable(HttpError):
    """406: client requested response format not supported."""

    status_code = 406


class ProxyAuthenticationRequired(HttpError):
    """407: client must authenticate with proxy."""

    status_code = 407


class RequestTimeout(HttpError):
    """408: request timed out (client too slow or connection stalled)."""

    status_code = 408


class Conflict(HttpError):
    """409: conflict with current state (duplicate resource, version mismatch)."""

    status_code = 409


class Gone(HttpError):
    """410: resource used to exist but is permanently removed."""

    status_code = 410


class LengthRequired(HttpError):
    """411: missing required Content-Length header."""

    status_code = 411


class PreconditionFailed(HttpError):
    """412: preconditions in headers failed (If-Match, If-Unmodified-Since)."""

    status_code = 412


class PayloadTooLarge(HttpError):
    """413: request body too large."""

    status_code = 413


class URITooLong(HttpError):
    """414: request URL too long."""

    status_code = 414


class UnsupportedMediaType(HttpError):
    """415: request content-type not supported."""

    status_code = 415


class RangeNotSatisfiable(HttpError):
    """416: invalid Range header for partial content."""

    status_code = 416


class ExpectationFailed(HttpError):
    """417: server cannot meet Expect header requirements."""

    status_code = 417


class ImATeapot(HttpError):
    """418: playful/experimental; rarely used."""

    status_code = 418


class MisdirectedRequest(HttpError):
    """421: request sent to wrong server (e.g., SNI mismatch)."""

    status_code = 421


class UnprocessableEntity(HttpError):
    """422: semantic errors (validation OK but business rules fail)."""

    status_code = 422


class Locked(HttpError):
    """423: resource locked (e.g., editing lock)."""

    status_code = 423


class FailedDependency(HttpError):
    """424: dependent request failed (WebDAV or chained operations)."""

    status_code = 424


class TooEarly(HttpError):
    """425: request risk of replay (early data)."""

    status_code = 425


class UpgradeRequired(HttpError):
    """426: client must switch protocol (e.g., require TLS)."""

    status_code = 426


class PreconditionRequired(HttpError):
    """428: server requires precondition (If-Match)."""

    status_code = 428


class TooManyRequests(HttpError):
    """429: rate limit exceeded."""

    status_code = 429


class RequestHeaderFieldsTooLarge(HttpError):
    """431: headers too large."""

    status_code = 431


class UnavailableForLegalReasons(HttpError):
    """451: access denied for legal reasons (geo/legal restriction)."""

    status_code = 451


# =========================
# 5xx Server Errors
# =========================


class InternalServerError(HttpError):
    """500: unexpected server error (bug or unhandled)."""

    status_code = 500


class NotImplemented(HttpError):
    """501: feature not implemented on server."""

    status_code = 501


class BadGateway(HttpError):
    """502: invalid response from upstream server."""

    status_code = 502


class ServiceUnavailable(HttpError):
    """503: service temporarily unavailable (maintenance, overload)."""

    status_code = 503


class GatewayTimeout(HttpError):
    """504: upstream server timeout."""

    status_code = 504


class HTTPVersionNotSupported(HttpError):
    """505: server doesn't support HTTP protocol version."""

    status_code = 505


class VariantAlsoNegotiates(HttpError):
    """506: transparent content negotiation error."""

    status_code = 506


class InsufficientStorage(HttpError):
    """507: server out of storage (WebDAV)."""

    status_code = 507


class LoopDetected(HttpError):
    """508: infinite loop detected (WebDAV)."""

    status_code = 508


class NotExtended(HttpError):
    """510: further extensions required."""

    status_code = 510


class NetworkAuthenticationRequired(HttpError):
    """511: client must authenticate to gain network access."""

    status_code = 511
