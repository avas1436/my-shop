from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from kavenegar import APIException, HTTPException as KHTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.core.sms_service import send_sms
from app.modules.users.models import User
from app.modules.users.schemas import (
    LoginWithPassword,
    OTPVerify,
    Register,
    RequestOTP,
    TokenResponse,
    UserGet,
)
from app.modules.users.service import request_otp_service, verify_otp_service

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

        # print(code)

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
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify OTP and issue access token",
)
async def verify_otp_route(
    request: Request,
    data: OTPVerify,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    device_id = request.headers.get("device-id", "unknown")

    token = await verify_otp_service(
        db=db,
        data=data,
        ip_address=ip,
        user_agent=user_agent,
        device_id=device_id,
    )

    return TokenResponse(access_token=token)


# ==============================================================================
# Complete Rgister
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
    current_user: Annotated[User, Depends(get_current_user)],  # JWT guard
) -> User:

    currnet, is_new = current_user

    if not is_new:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already completed",
        )

    hashed_password = hash_password(password=data.password.get_secret_value())

    currnet.first_name = data.first_name
    currnet.last_name = data.last_name
    currnet.birth_date = data.birth_date
    currnet.hashed_password = hashed_password

    try:
        await db.commit()
        await db.refresh(currnet)

    except SQLAlchemyError:
        db.rollback()
        raise

    return currnet


# ==============================================================================
# Login with Password
# ==============================================================================
@router.post(
    "/login/password",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login with password",
)
async def login_with_password(
    data: LoginWithPassword,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    # Find user
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

    token = create_access_token(subject=user.phone_number, is_new=False)

    return TokenResponse(access_token=token)


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
    current_user: Annotated[User, Depends(get_current_user)],  # JWT guard
) -> User:

    currnet, is_new = current_user

    if is_new:
        raise HTTPException(
            status_code=403,
            detail="complete your profile first",
        )

    return currnet
