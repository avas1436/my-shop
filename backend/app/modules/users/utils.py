# phone number validator
import re


def validate_phone(phone_number: str):
    if phone_number is None:
        return phone_number

    # تبدیل اعداد فارسی
    persian = "۰۱۲۳۴۵۶۷۸۹"
    english = "0123456789"
    table = str.maketrans(persian, english)
    phone_number = phone_number.translate(table)

    # حذف کاراکترهای غیر عدد
    phone_number = re.sub(r"\D", "", phone_number)

    # normalize
    if phone_number.startswith("989"):
        phone_number = "0" + phone_number[2:]
    elif phone_number.startswith("98"):
        phone_number = "0" + phone_number[2:]
    elif phone_number.startswith("9") and len(phone_number) == 10:
        phone_number = "0" + phone_number

    if not re.fullmatch(r"09\d{9}", phone_number):
        raise ValueError("Phone number must be a valid Iranian mobile number")

    return phone_number