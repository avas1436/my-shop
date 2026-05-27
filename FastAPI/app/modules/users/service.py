# app/modules/users/services.py
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.common.enums import PurposeOTP
from app.common.request_meta import ClientMeta
from app.config.settings import get_settings
from app.core.otp_service import create_otp, verify_otp
from app.core.security import (
    get_token_payload,
    hash_password,
    verify_password,
)
from app.errors.errors import (
    BadRequest,
    HttpError,
    InternalServerError,
    TooManyRequests,
    Unauthorized,
)
from app.modules.users.models import User
from app.modules.users.repository import RefreshTokenCache, UserRepository
from app.modules.users.schemas import (
    LoginWithPassword,
    OTPVerify,
    Register,
    RequestOTP,
    TokenPair,
)
from app.modules.users.utils import issue_access_token, issue_refresh_token

settings = get_settings()


# =========================
# User Services
# =========================
class AuthService:
    def __init__(
        self,
        db: AsyncSession,
        cache: RedisCache,
        meta: ClientMeta,
        ttl: int,
    ):
        self.db = db
        self.repo = UserRepository(db=db)
        self.cache = RefreshTokenCache(cache=cache, ttl_seconds=ttl)
        self.meta = meta

    # ============================================
    # Register User or Login
    # ============================================
    async def request_otp_service(
        self,
        data: RequestOTP,
    ):

        user = await self.repo.get_by_phone(phone_number=data.phone_number)

        if user and data.purpose == PurposeOTP.REGISTER:
            raise BadRequest(
                message="User with this phone number already registered.",
                code="REGISTERED",
            )

        if not user and data.purpose in (PurposeOTP.LOGIN, PurposeOTP.RESET):
            raise BadRequest(
                message="User not found",
                code="USER_NOT_FOUND",
            )

        code, wait = await create_otp(
            db=self.db,
            phone_number=data.phone_number,
            ip_address=self.meta.ip,
            user_agent=self.meta.user_agent,
            device_id=self.meta.device_id,
            purpose=data.purpose,
        )

        if wait:
            await self.repo.rollback()
            raise TooManyRequests(
                # message=f"please wait for {wait} seconds",
                message=f"""برای مدت
                {wait} 
                ثانیه صبر کنید""",
                code="RATE_LIMIT",
            )

        await self.repo.commit()

        return code

    # ============================================
    # verify OTP Code - Login with OTP Code
    # ============================================
    async def verify_otp_service(
        self,
        data: OTPVerify,
    ) -> TokenPair:

        is_valid = await verify_otp(
            db=self.db,
            phone=data.phone_number,
            ip_address=self.meta.ip,
            user_agent=self.meta.user_agent,
            device_id=self.meta.device_id,
            purpose=data.purpose,
            code=data.code,
        )

        if not is_valid:
            raise BadRequest(
                message="Invalid or expired OTP",
                code="INVALID_OTP",
            )

        user = await self.repo.get_by_phone(phone_number=data.phone_number)

        if data.purpose == PurposeOTP.REGISTER and user is not None:
            raise BadRequest(
                message="User with this phone number already registered.",
                code="ALREADY_EXIST_USER",
            )

        if data.purpose in (PurposeOTP.LOGIN, PurposeOTP.RESET) and user is None:
            raise BadRequest(
                message="User not found.",
                code="USER_NOT_FOUND",
            )

        if not user:
            user = await self.repo.create_user(phone_number=data.phone_number)
            await self.repo.commit()
            await self.repo.refresh(user)
        else:
            changed = self.repo.mark_verified(user=user) and self.repo.update_login(
                user=user
            )

            if changed:
                await self.repo.commit()

        refresh = await issue_refresh_token(user=user, cache=self.cache)
        access = await issue_access_token(user=user)

        return TokenPair(access_token=access, refresh_token=refresh)

    # ============================================
    # Login with password
    # ============================================
    async def login_with_password_service(
        self,
        data: LoginWithPassword,
    ) -> TokenPair:

        user = await self.repo.get_by_phone(phone_number=data.phone_number)

        if not user or not verify_password(
            password=data.password,
            hashed_password=user.hashed_password,
        ):
            raise BadRequest(
                message="User not found.",
                code="USER_NOT_FOUND",
            )

        if not user.hashed_password:
            raise BadRequest(
                message="This account doest activate password",
                code="NOT_ACTIVATE_PASSWORD",
            )

        # if not verify_password(
        #     password=data.password,
        #     hashed_password=user.hashed_password,
        # ):
        #     raise BadRequest(message="Invalid credentials", code="WRONG_credentials")

        update = self.repo.update_login(user=user)
        if not update:
            raise InternalServerError(message="Failed to update last login")

        await self.repo.commit()

        refresh = await issue_refresh_token(user=user, cache=self.cache)
        access = await issue_access_token(user=user)

        return TokenPair(access_token=access, refresh_token=refresh)

    # ============================================
    # Complete Register for new users
    # ============================================
    async def complete_register_service(
        self,
        data: Register,
        current_user: User,
    ) -> User:

        if not (
            current_user.first_name is None
            or current_user.last_name is None
            or current_user.hashed_password is None
        ):
            raise BadRequest("Profile already completed")

        hashed = hash_password(password=data.password.get_secret_value())

        try:
            await self.repo.complete_profile(
                user=current_user,
                first_name=data.first_name,
                last_name=data.last_name,
                birth_date=data.birth_date,
                hashed_password=hashed,
            )
            await self.repo.commit()
            await self.repo.refresh(current_user)
            return current_user

        except HttpError:
            await self.repo.rollback()
            raise

        except Exception:
            await self.repo.rollback()
            raise InternalServerError("Unexpected error") from None

    # ============================================
    # Refresh Token Service
    # ============================================
    async def refresh_token_service(
        self,
        refresh_token: str,
    ) -> TokenPair:

        payload = get_token_payload(refresh_token, expected_type="refresh")
        subject = str(payload["sub"])
        token_id = str(payload["jti"])

        is_active = await self.cache.is_active(
            jti=token_id,
            subject=subject,
        )
        if not is_active:
            raise Unauthorized("Refresh token is invalid or revoked")

        user = await self.repo.get_by_phone(phone_number=subject)

        if not user or not user.is_active or user.deleted_at is not None:
            await self.cache.revoke(jti=token_id, subject=subject)
            raise Unauthorized("User not found or inactive")

        await self.cache.revoke(jti=token_id, subject=subject)

        refresh = await issue_refresh_token(user=user, cache=self.cache)
        access = await issue_access_token(user=user)

        return TokenPair(access_token=access, refresh_token=refresh)

    # ============================================
    # Revoke Refresh Token
    # ============================================
    async def revoke_refresh_token_service(
        self,
        refresh_token: str,
    ) -> None:

        payload = get_token_payload(refresh_token, expected_type="refresh")
        token_id = str(payload["jti"])
        subject = str(payload["sub"])

        await self.cache.revoke(jti=token_id, subject=subject)

    # ============================================
    # Revoke All of Active Refresh Tokens
    # ============================================
    async def revoke_all_refresh_tokens_for_subject_service(
        self,
        phone_number: str,
    ) -> None:

        await self.cache.revoke(phone_number=phone_number)
