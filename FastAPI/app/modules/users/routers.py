# app/modules/users/routers.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.responses import SuccessAPIRoute, SuccessMessage
from app.modules.users.dependencies import get_auth_service
from app.modules.users.models import User
from app.modules.users.schemas import (
    AccessToken,
    LoginWithPassword,
    OTPVerify,
    Register,
    RequestOTP,
    UserGet,
)
from app.modules.users.service import (
    AuthService,
)
from app.modules.users.utils import (
    delete_refresh_token_cookie,
    get_refresh_token,
    set_refresh_token_cookie,
)

router = APIRouter(route_class=SuccessAPIRoute)


# ====================================================================
# Register User or Login
# ====================================================================
@router.post(
    "/otp/request",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessMessage,
)
async def request_otp(
    data: RequestOTP,
    service: Annotated[AuthService, Depends(get_auth_service)],
    # background: BackgroundTasks,
):

    code = await service.request_otp_service(data=data)

    print(code)

    # background.add_task(
    #     send_sms,
    #     receptor=data.phone_number,
    #     code=code,
    # )

    # enqueue در celery
    from app.tasks.sms import send_sms_task

    send_sms_task.delay(receptor=data.phone_number, code=code)

    return SuccessMessage(message="OTP sent successfully")


# ====================================================================
# verify OTP Code
# ====================================================================
@router.post(
    "/otp/verify",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
    summary="Verify OTP and issue token pair",
)
async def verify_otp_route(
    response: Response,
    data: OTPVerify,
    service: Annotated[AuthService, Depends(get_auth_service)],
):

    token_pair = await service.verify_otp_service(data=data)

    set_refresh_token_cookie(
        response=response,
        refresh_token=token_pair.refresh_token,
    )

    return AccessToken(access_token=token_pair.access_token)


# ====================================================================
# Complete Register
# ====================================================================
@router.post(
    "/register/complete",
    response_model=UserGet,
    status_code=status.HTTP_200_OK,
    summary="Complete register after first login",
)
async def register_complete(
    data: Register,
    service: Annotated[AuthService, Depends(get_auth_service)],
    current_user: Annotated[
        User,
        Depends(
            require_access(
                require_recent_login_within=timedelta(minutes=30),
                profile_required_fields=("phone_number",),
            )
        ),
    ],
):

    return await service.complete_register_service(
        data=data,
        current_user=current_user,
    )


# ====================================================================
# Login with Password
# ====================================================================
@router.post(
    "/login/password",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
    summary="Login with password",
)
async def login_with_password(
    response: Response,
    data: LoginWithPassword,
    service: Annotated[AuthService, Depends(get_auth_service)],
):

    token_pair = await service.login_with_password_service(data=data)

    set_refresh_token_cookie(
        response=response,
        refresh_token=token_pair.refresh_token,
    )

    return AccessToken(access_token=token_pair.access_token)


# ====================================================================
# Refresh both tokens
# ====================================================================
@router.post(
    "/token/refresh",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
    summary="Refresh access and refresh tokens",
)
async def refresh_token(
    response: Response,
    token: Annotated[str, Depends(get_refresh_token)],
    service: Annotated[AuthService, Depends(get_auth_service)],
):

    token_pair = await service.refresh_token_service(refresh_token=token)

    set_refresh_token_cookie(
        response=response,
        refresh_token=token_pair.refresh_token,
    )

    return AccessToken(access_token=token_pair.access_token)


# ====================================================================
# Logout and remove refresh token from redis
# ====================================================================
@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=SuccessMessage,
    summary="Revoke current refresh token",
)
async def logout(
    response: Response,
    token: Annotated[str, Depends(get_refresh_token)],
    service: Annotated[AuthService, Depends(get_auth_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                require_recent_login_within=timedelta(days=15),
            )
        ),
    ],
):
    await service.revoke_refresh_token_service(refresh_token=token)

    delete_refresh_token_cookie(response=response)

    return SuccessMessage(message="Logged out successfully")


# ====================================================================
# New Feature: Logout all sessions
# ====================================================================
@router.post(
    "/logout/all",
    status_code=status.HTTP_200_OK,
    response_model=SuccessMessage,
    summary="Revoke all refresh tokens for current user",
)
async def logout_all(
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
    phone_number: str,
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=7),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):
    await service.revoke_all_refresh_tokens_for_subject_service(
        phone_number=phone_number,
    )

    delete_refresh_token_cookie(response=response)

    return SuccessMessage(message="Logged out from all devices successfully")


# ====================================================================
# Get current user
# ====================================================================
@router.get(
    "/me",
    response_model=UserGet,
    status_code=status.HTTP_200_OK,
    summary="Get User Status",
)
def me(
    current_user: Annotated[
        User,
        Depends(
            require_access(
                require_recent_login_within=timedelta(days=15),
                # require_password=True,
                # require_profile_complete=True,
                # profile_required_fields=("first_name", "last_name"),
            )
        ),
    ],
):

    return current_user
