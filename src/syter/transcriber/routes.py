from flask import Blueprint, request, abort

from .rev_ai import Transcriber

transcriber_bp = Blueprint("transcriber", __name__, url_prefix="/transcriber")


@transcriber_bp.post("")
def submit_audio() -> dict:
    """
    Given a link to the audio file and source language code,
    Submit job to RevAI
    """

    link = request.form.get("link")
    language_code = request.form.get("language_code")

    if not link or not language_code:
        abort(401, description="Required parameters are 'link' and 'language_code'")

    transcriber = Transcriber(language_code)
    id = transcriber.submit_job(link)

    return {
        "status": "in_progress",
        "job_id": id
    }
