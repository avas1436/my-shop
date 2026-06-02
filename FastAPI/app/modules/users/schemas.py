# app/modules/users/schemas.py
from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    StringConstraints,
    ValidationInfo,
    computed_field,
    field_validator,
)

from app.common.enums import PurposeOTP
from app.modules.users.utils import validate_password, validate_phone


# ==============================================================================
# Register User or Login
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
class OTPVerify(BaseModel):
    phone_number: str
    code: Annotated[str, StringConstraints(min_length=4, max_length=6)]
    purpose: PurposeOTP = Field(default=PurposeOTP.LOGIN)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str):
        return validate_phone(phone_number=v)


# ==============================================================================
# Rgister
# ==============================================================================
class Register(BaseModel):
    first_name: str
    last_name: str
    birth_date: date | None = None
    password: SecretStr = Field(..., min_length=8, max_length=64)
    password_confirm: SecretStr = Field(..., min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, v: SecretStr):
        validate_password(v.get_secret_value())
        return v

    @field_validator("password_confirm")
    @classmethod
    def verify_passwords_match(cls, v: SecretStr, info: ValidationInfo):
        if "password" in info.data:
            pwd = info.data["password"].get_secret_value()
            pwd_confirm = v.get_secret_value()

            if pwd != pwd_confirm:
                raise ValueError("Password and password confirmation do not match")

        return v

    model_config = ConfigDict(
        extra="forbid",  # Mass Assignment Attack
        str_strip_whitespace=True,  # strip string
    )


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
    first_name: str | None
    last_name: str | None
    birth_date: date | None


# ==============================================================================
# Get User
# ==============================================================================
class UserGet(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    phone_number: str
    birth_date: date | None
    is_phone_verified: bool
    role: str
    is_active: bool
    created_at: datetime

    @computed_field
    @property
    def age(self) -> int | None:
        if self.birth_date is None:
            return None

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
# Access Token
# ==============================================================================
class AccessToken(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


# ==============================================================================
# Pair Token
# ==============================================================================
class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"
