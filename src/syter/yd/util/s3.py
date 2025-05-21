import boto3
from io import BytesIO
from botocore.config import Config
from botocore.exceptions import ClientError


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
                         object_name: str) -> str | None:
        assert isinstance(data, BytesIO)
        assert type(object_name) is str

        # TODO: Check if already exists in bucket

        try:
            self._client.upload_fileobj(data,
                                        S3.BUCKET_NAME,
                                        object_name)
        except ClientError as e:
            print(e)
            return None

        return object_name

    def get_presigned_link(self,
                           object_name: str,
                           expires_in: int = 3600) -> str | None:
        assert type(object_name) is str
        assert type(expires_in) is int and expires_in > 0

        try:
            url = self._client.generate_presigned_url("get_object",
                                                      Params={
                                                          "Bucket": S3.BUCKET_NAME,
                                                          "Key": object_name
                                                      },
                                                      ExpiresIn=expires_in)
            return url
        except ClientError as e:
            print(e)
            return None
