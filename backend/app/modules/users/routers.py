from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from kavenegar import APIException, HTTPException as KHTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.core.redis import get_redis_client
from app.core.security import hash_password, verify_password
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
    issue_token_pair,
    refresh_token_service,
    request_otp_service,
    revoke_refresh_token_service,
    verify_otp_service,
)

router = APIRouter()


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
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    device_id = request.headers.get("device-id", "unknown")

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

        return {"message": "OTP sent successfully"}

    except APIException as e:
        raise HTTPException(status_code=400, detail=str(e)) from None

    except KHTTPException as e:
        raise HTTPException(status_code=502, detail=str(e)) from None

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from None


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
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    device_id = request.headers.get("device-id", "unknown")

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
async def register(
    data: Register,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.first_name is not None:
        raise HTTPException(
            status_code=400,
            detail="Profile already completed",
        )

    hashed_password = hash_password(password=data.password.get_secret_value())

    current_user.first_name = data.first_name
    current_user.last_name = data.last_name
    current_user.birth_date = data.birth_date
    current_user.hashed_password = hashed_password

    try:
        await db.commit()
        await db.refresh(current_user)

    except SQLAlchemyError:
        await db.rollback()
        raise

    return current_user


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
    stmt = select(User).where(User.phone_number == data.phone_number).limit(1)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials",
        )

    if not verify_password(
        password=data.password,
        hashed_password=user.hashed_password,
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials",
        )

    return await issue_token_pair(
        user=user,
        redis_client=get_redis_client(request),
    )


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


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Revoke current refresh token",
)
async def logout(
    request: Request,
    data: RefreshTokenRequest,
):
    await revoke_refresh_token_service(
        refresh_token=data.refresh_token,
        redis_client=get_redis_client(request),
    )
    return {"message": "Logged out successfully"}


# ==============================================================================
# Get User
# ==============================================================================
@router.get(
    "/me",
    response_model=UserGet,
    status_code=status.HTTP_200_OK,
    summary="Get User Status",
)
def me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.first_name is None:
        raise HTTPException(
            status_code=403,
            detail="complete your profile first",
        )

    return current_user
