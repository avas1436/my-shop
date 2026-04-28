from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from kavenegar import APIException, HTTPException as KHTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.access_control import require_access
from app.common.responses import success_response
from app.core.database import get_db
from app.core.redis import get_redis_client
from app.core.sms_service import send_sms
from app.modules.users.models import User
from app.modules.users.schemas import (
    LoginWithPassword,
    OTPVerify,
    RefreshTokenRequest,
    Register,
    RequestOTP,
    TokenPair,
    UserGet,
)
from app.modules.users.service import (
    complete_register_service,
    login_with_password_service,
    refresh_token_service,
    request_otp_service,
    revoke_all_refresh_tokens_for_subject_service,
    revoke_refresh_token_service,
    verify_otp_service,
)

router = APIRouter()


# ==============================================================================
# Get Meta Data from request
# ==============================================================================
def _client_meta(request: Request) -> tuple[str, str, str]:
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    device_id = request.headers.get("device-id", "unknown")
    return ip, user_agent, device_id


# ==============================================================================
# Register User or Login
# ==============================================================================
@router.post(
    "/otp/request",
    status_code=status.HTTP_201_CREATED,
)
async def request_otp(
    request: Request,
    data: RequestOTP,
    db: Annotated[AsyncSession, Depends(get_db)],
    background: BackgroundTasks,
):
    ip, user_agent, device_id = _client_meta(request)

    try:
        code, wait = await request_otp_service(
            db=db,
            phone_number=data.phone_number,
            purpose=data.purpose,
            ip_address=ip,
            user_agent=user_agent,
            device_id=device_id,
        )

        if wait:
            raise HTTPException(
                status_code=429,
                detail=f"please wait for {wait} seconds",
            )

        background.add_task(
            send_sms,
            receptor=data.phone_number,
            code=code,
        )

        return success_response(message="OTP sent successfully")

    except APIException as e:
        raise HTTPException(status_code=400, detail=str(e)) from None

    except KHTTPException as e:
        raise HTTPException(status_code=502, detail=str(e)) from None

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e)) from None


# ==============================================================================
# verify OTP Code
# ==============================================================================
@router.post(
    "/otp/verify",
    response_model=TokenPair,
    status_code=status.HTTP_200_OK,
    summary="Verify OTP and issue token pair",
)
async def verify_otp_route(
    request: Request,
    data: OTPVerify,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    ip, user_agent, device_id = _client_meta(request)

    return await verify_otp_service(
        db=db,
        data=data,
        ip_address=ip,
        user_agent=user_agent,
        device_id=device_id,
        redis_client=get_redis_client(request),
    )


# ==============================================================================
# Complete Register
# ==============================================================================
@router.post(
    "/register/complete",
    response_model=UserGet,
    status_code=status.HTTP_200_OK,
    summary="Complete register after first login",
)
async def register_complete(
    data: Register,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_access())],
) -> User:
    return await complete_register_service(
        db=db,
        current_user=current_user,
        data=data,
    )


# ==============================================================================
# Login with Password
# ==============================================================================
@router.post(
    "/login/password",
    response_model=TokenPair,
    status_code=status.HTTP_200_OK,
    summary="Login with password",
)
async def login_with_password(
    request: Request,
    data: LoginWithPassword,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await login_with_password_service(
        db=db,
        data=data,
        redis_client=get_redis_client(request),
    )


# ==============================================================================
# Login with Password
# ==============================================================================
@router.post(
    "/token/refresh",
    response_model=TokenPair,
    status_code=status.HTTP_200_OK,
    summary="Refresh access and refresh tokens",
)
async def refresh_token(
    request: Request,
    data: RefreshTokenRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await refresh_token_service(
        db=db,
        refresh_token=data.refresh_token,
        redis_client=get_redis_client(request),
    )


# ==============================================================================
# Logout and remove refresh token from redis
# ==============================================================================
@router.post(
    "/logout", status_code=status.HTTP_200_OK, summary="Revoke current refresh token"
)
async def logout(
    request: Request,
    data: RefreshTokenRequest,
):
    await revoke_refresh_token_service(
        refresh_token=data.refresh_token,
        redis_client=get_redis_client(request),
    )
    return success_response(message="Logged out successfully")


# ==============================================================================
# New Feature: Logout all sessions
# ==============================================================================
@router.post(
    "/logout/all",
    status_code=status.HTTP_200_OK,
    summary="Revoke all refresh tokens for current user",
)
async def logout_all(
    request: Request,
    current_user: Annotated[User, Depends(require_access())],
):
    await revoke_all_refresh_tokens_for_subject_service(
        redis_client=get_redis_client(request),
        subject=str(current_user.phone_number),
    )
    return success_response(message="Logged out from all devices successfully")


# ==============================================================================
# Get current user
# ==============================================================================
@router.get(
    "/me",
    response_model=UserGet,
    status_code=status.HTTP_200_OK,
    summary="Get User Status",
)
def me(
    current_user: Annotated[User, Depends(require_access())],
) -> User:

    return current_user
