from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(
    app: FastAPI,
    allow_origins: list[str],
    allow_credentials: bool,
    allow_methods: list[str],
    allow_headers: list[str],
    expose_headers: list[str],
    max_age: int,
) -> None:

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,  # چه دامنه هایی اجازه وصل شدن دارند
        allow_credentials=allow_credentials,  # اجازه فعالیت سشن و کوکی و بقیه چیزا
        allow_methods=allow_methods,  # HTTP Methods
        allow_headers=allow_headers,  # چه هدر هایی مجازن درخواست بدن
        expose_headers=expose_headers,  # چه هدر هایی به جاوا اسکریپت نشون داده بشه
        max_age=max_age,  # مدت زمان کش پری فلایت مرورگر
    )
