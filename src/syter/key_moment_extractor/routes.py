from flask import Blueprint, request, abort

from .kme import KeyMomentExtractor

kme_bp = Blueprint("kme", __name__, url_prefix="/kme")


@kme_bp.post("")
def get_key_moments() -> dict:
    json: dict = request.get_json()

    title = json["title"]
    description = json["description"]
    transcript: dict = json["transcript"]
    sentences = transcript["sentences"]

    key_moments = KeyMomentExtractor().extract(
        title,
        description,
        [s["text"] for s in sentences]
    )

    return {
        "count": len(key_moments),
        "shorts": [
            {
                "caption": km.caption,
                "segments": [
                    {
                        "start_time": sentences[i]["start_time"],
                        "end_time": sentences[i]["end_time"],
                        "text": sentences[i]["text"]
                    }
                    for i in km.segments
                ],
            }
            for km in key_moments
        ]
    }
