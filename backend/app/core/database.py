from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import get_settings

settings = get_settings()

# انجین خود دیتا بیس نیست بلکه راه ورود و قوانین ورود به دیتابیس توسط برنامه است
engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=settings.db_pool_timeout,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=settings.db_pool_pre_ping,
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


async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
