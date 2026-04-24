from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from kavenegar import APIException, HTTPException as KHTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import PurposeOTP
from app.core.database import get_db
from app.core.otp_service import create_otp, verify_otp
from app.core.security import create_access_token
from app.core.sms_service import send_sms
from app.modules.users.models import User
from app.modules.users.schemas import OTPVerify, RequestOTP, TokenResponse

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
    purpose: PurposeOTP,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    # اگر هدف ثبت‌نام است و کاربر وجود دارد -> خطا
    if purpose == PurposeOTP.register:
        stmt_user = select(User).where(User.phone_number == data.phone_number)
        res_user = await db.execute(stmt_user)
        user = res_user.scalar_one_or_none()
        if user:
            raise HTTPException(400, detail="این شماره قبلاً ثبت‌نام شده است")

    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    device_id = request.headers.get("device-id", "unknown")

    try:
        code, wait = await create_otp(
            db=db,
            phone_number=data.phone_number,
            ip_address=ip,
            user_agent=user_agent,
            device_id=device_id,
            purpose=purpose,
        )

        if wait:
            raise HTTPException(
                status_code=429,
                detail=f"please wait for {wait} seconds",
            )

        # ارسال پیامک به صورت async
        await send_sms(
            receptor=data.phone_number,
            code=code,
        )

        return {"message": "OTP sent successfully"}

    except APIException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from None

    except KHTTPException as e:
        raise HTTPException(
            status_code=502,
            detail=str(e),
        ) from None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from None


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

    # 1) Verify OTP
    is_valid = await verify_otp(
        db=db,
        phone=data.phone_number,
        ip_address=ip,
        user_agent=user_agent,
        device_id=device_id,
        purpose=data.purpose,
        code=data.code,
    )

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP",
        )

    # 2) Find user
    stmt = select(User).where(User.phone_number == data.phone_number)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    # 3) Purpose-aware user handling
    if not user:
        user = User(
            phone_number=data.phone_number,
            is_phone_verified=True,
            last_login=datetime.now(UTC),
        )
        db.add(user)
        try:
            await db.commit()
            await db.refresh(user)
        except IntegrityError:
            # اگر همزمان یک درخواست دیگر کاربر را ساخت
            await db.rollback()
            result = await db.execute(
                select(User).where(User.phone_number == data.phone_number).limit(1)
            )
            user = result.scalar_one_or_none()
            if user is None:
                raise HTTPException(
                    status_code=500,
                    detail="Could not finalize user authentication",
                ) from None

    else:
        changed = False

        if not user.is_phone_verified:
            user.is_phone_verified = True
            changed = True

        # آپدیت آخرین ورود
        if hasattr(user, "last_login_at"):
            user.last_login_at = datetime.now(UTC)
            changed = True

        if changed:
            await db.commit()

    token = create_access_token(subject=data.phone_number)

    return TokenResponse(access_token=token)


# @router.get("/me")
# async def read_current_user(
#     user_id: int = Depends(get_current_user_id),
# ) -> dict[str, int]:
#     return {"user_id": user_id}
