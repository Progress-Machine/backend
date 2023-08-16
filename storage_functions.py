from os import environ
from s3 import S3Client
from load_env import load_env

load_env()

identifier = environ.get("YANDEX_CLOUD_ID")
key = environ.get("YANDEX_CLOUD_KEY")
s3 = S3Client(
    access_key=identifier,
    secret_key=key,
    region='ru-central1',
    s3_bucket='first343203'
)


async def upload_file(path: str, file: bytes):
    await s3.upload(path, file)


def get_file_url(path: str) -> str:
    return s3.signed_download_url(path, max_age=60)


async def delete_file(path: str):
    await s3.delete(path)


def download_file(path: str):
    return s3.signed_download_url(path, max_age=60)


if __name__ == '__main__':
    # asyncio.run(delete_file(f"applications_file/1/Resume.pdf"))
    print(download_file(f"applications_file/1/Resume.pdf"))
