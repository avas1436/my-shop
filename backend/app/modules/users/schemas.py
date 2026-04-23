import datetime
from datetime import date
from typing import Annotated, Optional

from app.common.enums import PurposeOTP
from pydantic import (
    BaseModel,
    Field,
    StringConstraints,
    computed_field,
    field_validator,
)

from backend.app.modules.users.utils import validate_phone


# ==============================================================================
# Register User and Login
# ==============================================================================
class RequestOTP(BaseModel):
    phone_number: str
    purpose: PurposeOTP = Field(default=PurposeOTP.LOGIN)  # LOGIN | REGISTER | RESET

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str):
        return validate_phone(phone_number=v)


# ==============================================================================
# verify OTP Code
# ==============================================================================
class OTPCode(BaseModel):
    phone_number: str
    code: Annotated[str, StringConstraints(min_length=4, max_length=6)]
    purpose: PurposeOTP = Field(default=PurposeOTP.LOGIN)


# ==============================================================================
# Rgister
# ==============================================================================
class Rgister(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    password: Optional[str] = None


# ==============================================================================
# Password Login
# ==============================================================================
class LoginWithPassword(BaseModel):
    phone_number: str
    password: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str):
        return validate_phone(phone_number=v)


# ==============================================================================
# Update Profile
# ==============================================================================
class ProfileUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[date]


# ==============================================================================
# Get User
# ==============================================================================
class UserGet(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: str
    birth_date: Optional[date]
    is_phone_verified: bool
    role: str
    is_active: bool
    created_at: datetime

    @computed_field
    @property
    def age(self) -> Optional[int]:
        if self.birth_date is None:
            return self.birth_date

        today = date.today()
        age = (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

        return age

    class Config:
        from_attributes = True


# ==============================================================================
# Pait Token
# ==============================================================================
class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
