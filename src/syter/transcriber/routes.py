from flask import Blueprint, request, abort, url_for

from .rev_ai import Transcriber

transcriber_bp = Blueprint("transcriber", __name__, url_prefix="/transcriber")


@transcriber_bp.post("")
def submit_audio() -> dict:
    """
    Given a link to the audio file and source language code,
    Submit job to RevAI
    """

    link = request.args.get("link")
    language_code = request.args.get("language_code")

    if not link or not language_code:
        abort(400, description="Required parameters are 'link' and 'language_code'")

    transcriber = Transcriber(language_code, url_for(".done_transcribing"))
    id = transcriber.submit_job(link)

    return {
        "status": "in_progress",
        "job_id": id
    }


@transcriber_bp.post("/retrieve")
def done_transcribing() -> dict:
    """
    Invoked by Rev AI when transcription is completed
    """

    job = request.get_json()
    if not job:
        abort(400, description="Invalid request.")

    try:
        job_details = job["job"]

        job_id: str | None = job_details.get("id")
        if not job_id:
            abort(400, "Invalid request.")

        transcriber = Transcriber(job_details.get("language", "en-us"))
        if (transcript := transcriber.retrieve_transcript(job_id)):
            return {
                "id": job_id,
                "transcript": str(transcript)
            }
        else:
            abort(400, description="Transcript not found")
    except KeyError:
        abort(400, description="Invalid request")
