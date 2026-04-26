from datetime import UTC, datetime

from app.core.refresh_tokens import (
    is_refresh_token_active,
    revoke_refresh_token,
)
from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import PurposeOTP
from app.core.otp_service import create_otp, verify_otp
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_token_payload,
    store_refresh_token,
)
from app.modules.users.models import User
from app.modules.users.schemas import OTPVerify, TokenPair


def is_new_user(user: User) -> bool:
    return (
        user.first_name is None
        or user.last_name is None
        or user.hashed_password is None
    )


# =========================
# Refresh Flow
# =========================
async def issue_token_pair(user: User, redis_client: Redis | None) -> TokenPair:

    access_token = create_access_token(subject=user.phone_number)

    refresh_token = create_refresh_token(subject=user.phone_number)

    refresh_payload = get_token_payload(refresh_token, expected_type="refresh")

    await store_refresh_token(
        redis_client=redis_client,
        token_id=str(refresh_payload["jti"]),
        subject=user.phone_number,
    )

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )


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
        return None, wait

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
    redis_client: Redis | None = None,
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

    return await issue_token_pair(user=user, redis_client=redis_client)


async def refresh_token_service(
    db: AsyncSession,
    refresh_token: str,
    redis_client: Redis | None = None,
) -> TokenPair:
    payload = get_token_payload(refresh_token, expected_type="refresh")
    subject = str(payload["sub"])
    token_id = str(payload["jti"])

    if not await is_refresh_token_active(
        redis_client, token_id=token_id, subject=subject
    ):
        raise HTTPException(
            status_code=401,
            detail="Refresh token is invalid or revoked",
        )

    stmt = select(User).where(User.phone_number == subject).limit(1)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not user.is_active or user.deleted_at is not None:
        await revoke_refresh_token(redis_client, token_id=token_id)
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive",
        )

    await revoke_refresh_token(redis_client, token_id=token_id)
    return await issue_token_pair(user=user, redis_client=redis_client)


async def revoke_refresh_token_service(
    refresh_token: str,
    redis_client: Redis | None = None,
) -> None:
    try:
        payload = get_token_payload(refresh_token, expected_type="refresh")
    except ValueError:
        return

    await revoke_refresh_token(
        redis_client=redis_client,
        token_id=str(payload["jti"]),
    )
