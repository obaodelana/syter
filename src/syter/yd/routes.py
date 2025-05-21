from flask import Blueprint, request, abort
import requests
import os
from .video import Video
from .util.s3 import S3

yd_bp = Blueprint("yd", __name__, url_prefix="/yd")


@yd_bp.get("/<id>")
def submit_video(id: str) -> dict:
    """
    Get video details (title, thumbnail url, description, duration)
    from id using YouTube's Data API
    """

    api_key = os.getenv("YT_API_KEY", None)
    assert api_key is not None

    base_url = "https://youtube.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,contentDetails",
        "id": id,
        "fields": "items(snippet(title,description,thumbnails(maxres)),contentDetails(duration))",
        "key": api_key
    }
    headers = {"Content-Type": "application/json"}

    response = requests.get(base_url, params=params, headers=headers)
    print(response.url)
    try:
        response.raise_for_status()

        json = response.json()
        if "items" not in json\
                or type(json["items"]) is not list\
                or len(json["items"]) == 0:
            abort(500, description="Can not contact YouTube")

        video_info = json["items"][0]
        title = video_info["snippet"]["title"]
        description = video_info["snippet"]["description"]
        thumbnail_url = video_info["snippet"]["thumbnails"]["maxres"]["url"]
        duration = video_info["contentDetails"]["duration"]

        return {
            "id": id,
            "title": title,
            "description": description,
            "thumbnail_url": thumbnail_url,
            "duration": duration
        }

    except requests.exceptions.HTTPError as error:
        abort(response.status_code, description=str(error))


@yd_bp.post("/download-audio")
def download_audio() -> dict:
    """
    Given video id,
    Download video to S3 bucket and return pre-signed link
    """

    id = request.form.get("id")
    if not id:
        abort(401, description="Missing attribute 'id'")

    video = Video(id)
    bytes = video.open_audio()
    if not bytes.closed:
        s3 = S3()
        object_name = s3.upload_to_bucket(bytes, video.id)
        if not object_name:
            abort(500, description="Unable to upload audio")

        url = s3.get_presigned_link(object_name)
        if not url:
            abort(500, description="Unable to get presigned URL")

        bytes.close()

        return {"link": url}
    else:
        abort(500, description="Could not download file")


@yd_bp.post("/retrieve")
def retrieve_short() -> dict:
    """
    Given video id and key moments,
    Return link to zip file containing video clips
    """

    return {
        "link": ""
    }
