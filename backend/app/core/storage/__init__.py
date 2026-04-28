# app/core/storage/__init__.py

# from app.core.storage.cdn import S3AsyncStorage

from app.config.settings import get_settings
from app.core.storage.local import LocalAsyncStorage

settings = get_settings()


def get_storage():

    # این قسمت تعیین کننده روش ذخیره عکس است
    # if settings.STORAGE_BACKEND == "s3":
    #     return S3AsyncStorage()

    return LocalAsyncStorage()
