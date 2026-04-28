# # app/core/storage/s3.py
# import aioboto3

# from app.config.settings import get_settings

# settings = get_settings()


# class S3AsyncStorage:
#     async def save(
#         self, data: bytes, path: str, content_type: str | None = None
#     ) -> str:
#         session = aioboto3.Session()
#         async with session.client(
#             "s3",
#             endpoint_url=settings.S3_ENDPOINT,
#             aws_access_key_id=settings.S3_ACCESS_KEY,
#             aws_secret_access_key=settings.S3_SECRET_KEY,
#             region_name=settings.S3_REGION,
#         ) as s3:
#             kwargs = {"Bucket": settings.S3_BUCKET, "Key": path, "Body": data}
#             if content_type:
#                 kwargs["ContentType"] = content_type
#             await s3.put_object(**kwargs)
#         return path

#     async def delete(self, path: str) -> None:
#         session = aioboto3.Session()
#         async with session.client(
#             "s3",
#             endpoint_url=settings.S3_ENDPOINT,
#             aws_access_key_id=settings.S3_ACCESS_KEY,
#             aws_secret_access_key=settings.S3_SECRET_KEY,
#             region_name=settings.S3_REGION,
#         ) as s3:
#             await s3.delete_object(Bucket=settings.S3_BUCKET, Key=path)
