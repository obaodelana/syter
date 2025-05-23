from flask import Blueprint, request, abort, url_for

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
        abort(400, description="Required parameters are 'link' and 'language_code'")

    # TODO: Pass web hook url
    transcriber = Transcriber(language_code)
    id = transcriber.submit_job(link)

    return {
        "status": "in_progress",
        "job_id": id
    }


@transcriber_bp.post("/retrieve")
def retrieve_transcript() -> dict:
    """
    Invoked by Rev AI when transcription is completed
    """

    job = request.get_json()
    if not job:
        abort(400, description="Invalid request.")

    try:
        job_details: dict = job["job"]
        job_id = job_details["id"]
        job_language = job_details.get("language", "en-us")
    except KeyError:
        abort(400, description="Invalid request")

    transcriber = Transcriber(job_language)
    transcript = transcriber.retrieve_transcript(job_id)

    return {
        "id": job_id,
        "transcript": {
            "start_time": str(transcript.start_time),
            "end_time": str(transcript.end_time),
            "text": str(transcript.text),
            "sentences": [
                {
                    "start_time": str(transcript[i].start_time),
                    "end_time": str(transcript[i].end_time),
                    "text": transcript[i].text
                }
                for i in range(len(transcript))
            ]
        }
    }
