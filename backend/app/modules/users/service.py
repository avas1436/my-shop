from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import PurposeOTP
from app.core.otp_service import create_otp, verify_otp
from app.core.security import create_access_token
from app.modules.users.models import User
from app.modules.users.schemas import OTPVerify


# ==============================================================================
# Register User or Login
# ==============================================================================
async def request_otp_service(
    db: AsyncSession,
    phone_number: str,
    purpose: PurposeOTP,
    ip_address: str,
    user_agent: str,
    device_id: str,
):
    stmt_user = select(User).where(User.phone_number == phone_number)
    res_user = await db.execute(stmt_user)
    user = res_user.scalar_one_or_none()

    if user and purpose == PurposeOTP.REGISTER:
        raise HTTPException(400, detail="این شماره قبلاً ثبت‌نام شده است")

    if not user and (purpose == PurposeOTP.LOGIN or purpose == PurposeOTP.RESET):
        raise HTTPException(400, detail="کاربر یافت نشد")

    code, wait = await create_otp(
        db=db,
        phone_number=phone_number,
        ip_address=ip_address,
        user_agent=user_agent,
        device_id=device_id,
        purpose=purpose,
    )

    if wait:
        await db.rollback()
        return {"wait": wait}

    await db.commit()

    return code, wait


# ==============================================================================
# verify OTP Code
# ==============================================================================
async def verify_otp_service(
    db: AsyncSession,
    data: OTPVerify,
    ip_address: str,
    user_agent: str,
    device_id: str,
):
    # 1) Verify OTP
    is_valid = await verify_otp(
        db=db,
        phone=data.phone_number,
        ip_address=ip_address,
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
    stmt = select(User).where(User.phone_number == data.phone_number).limit(1)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    # 3) Purpose-aware user handling
    if not user:
        stmt = (
            insert(User)
            .values(
                phone_number=data.phone_number,
                is_phone_verified=True,
                last_login=datetime.now(UTC),
            )
            .on_conflict_do_nothing(index_elements=[User.phone_number])
            .returning(User.id)
        )
        res = await db.execute(stmt)
        user_id = res.scalar_one_or_none()
        await db.commit()

        if user_id is None:
            # یعنی کاربر از قبل وجود داشته، حالا بخونش
            res = await db.execute(
                select(User).where(User.phone_number == data.phone_number).limit(1)
            )
            user = res.scalar_one_or_none()
        else:
            # اگر خواستی شی کامل رو بگیری
            res = await db.execute(select(User).where(User.id == user_id))
            user = res.scalar_one()

    else:
        changed = False

        if not user.is_phone_verified:
            user.is_phone_verified = True
            changed = True

        if hasattr(user, "last_login"):
            user.last_login = datetime.now(UTC)
            changed = True

        if changed:
            await db.commit()

    is_new = user.first_name is None

    token = create_access_token(subject=data.phone_number, is_new=is_new)

    return token
