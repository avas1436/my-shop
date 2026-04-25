from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from kavenegar import APIException, HTTPException as KHTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.sms_service import send_sms
from app.modules.users.schemas import OTPVerify, RequestOTP, TokenResponse
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
