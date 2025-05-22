import boto3
from io import BytesIO
from botocore.config import Config
from datetime import datetime


class S3:
    BUCKET_NAME = "syter"

    def __init__(self) -> None:
        config = Config(
            region_name="us-east-2",
            signature_version="v4",
        )
        self._client = boto3.client("s3", config=config)

    def upload_to_bucket(self,
                         data: BytesIO,
                         name: str) -> str:
        assert isinstance(data, BytesIO)
        assert type(name) is str

        object_name = f"[{datetime.now()}] {name}"
        self._client.upload_fileobj(data,
                                    S3.BUCKET_NAME,
                                    object_name)

        return object_name

    def get_presigned_link(self,
                           object_name: str,
                           expires_in: int = 3600) -> str:
        assert type(object_name) is str
        assert type(expires_in) is int and expires_in > 0

        url = self._client.generate_presigned_url("get_object",
                                                  Params={
                                                      "Bucket": S3.BUCKET_NAME,
                                                      "Key": object_name
                                                  },
                                                  ExpiresIn=expires_in)
        return url
