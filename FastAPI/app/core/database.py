# app/core/database.py
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import get_settings

settings = get_settings()

# انجین خود دیتا بیس نیست بلکه راه ورود و قوانین ورود به دیتابیس توسط برنامه است
engine = create_async_engine(
    settings.database_url,
    echo=False,  # چاپ کویری های دیتابیس در کنسول
    future=True,
    pool_size=settings.db_pool_size,  # تعداد اتصالات همزمان فعال در دیتا بیس
    max_overflow=settings.db_max_overflow,  # حداکثر اتصال در زمان اوج ترافیک
    pool_timeout=settings.db_pool_timeout,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=settings.db_pool_pre_ping,  # یک تست ساده پینگ قبل از اتصال
)


# اگر انجین قالب کیک باشد سشن میکر خود کیک است ولی همین جوری نمی خوریمش و میدیمش
# به یک تابع امن که به  محض استفاده بسته بشه
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


# بیس در اصل یک کلاس است که تنها ویژگی آن ژن مشترک تمامی مدل های آینده است
# یعنی تنها کلاس هایی که از بیس ارث میبرند میتوانن در دیتابیس جدول تشکیل دهند
# به عبارتی ساختمان نیست بلکه نقشه آن است.
class Base(DeclarativeBase):
    pass


# async def get_db() -> AsyncIterator[AsyncSession]:
#     async with AsyncSessionLocal() as session:
#         yield session


# در این نسخه در صورتی که بین انجام یک درخواست اروری اینجاد شود
# حتی در صورتی که داخل کد برای ارور ها رول بک تعیین نشده باشد
# در این لایه به صورت خودکار رول بک زده میشود
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
