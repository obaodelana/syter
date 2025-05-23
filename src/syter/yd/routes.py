from flask import Blueprint, request, abort
from .video import Video
from .util.s3 import S3

yd_bp = Blueprint("yd", __name__, url_prefix="/yd")


@yd_bp.post("/download-audio")
def download_audio() -> dict:
    """
    Given video id,
    Download video to S3 bucket and return pre-signed link
    """

    id = request.form.get("id")
    if not id:
        abort(400, description="Missing attribute 'id'")

    video = Video(id)
    with video.open_audio() as bytes:
        s3 = S3()
        object_name = s3.upload_to_bucket(bytes, video.id)
        url = s3.get_presigned_link(object_name)

    return {"link": url}


@yd_bp.post("/short")
def download_short() -> dict:
    """
    Given video id and key moments,
    Return link to zip file containing video clips
    """

    return {
        "link": ""
    }
