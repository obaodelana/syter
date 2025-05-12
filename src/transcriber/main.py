import os
from rev_ai import apiclient, CustomerUrlData, JobStatus

from models.transcript import Transcript


class Transcriber:
    def __init__(self, language: str, webhook_url: str) -> None:
        assert type(language) is str
        assert type(webhook_url) is str

        api_key = os.getenv("REV_API_KEY")
        if not api_key:
            raise Exception("Can not find environment variable 'REV_API_KEY'")

        self.language = language
        self._callback_url = webhook_url
        self._client = apiclient.RevAiAPIClient(api_key)

    def submit_file(self, url: str) -> int:
        assert type(url) is str

        job = self._client.submit_job_url(
            language=self.language,
            transcriber="low_cost",
            notification_config=CustomerUrlData(url=self._callback_url),
            source_config=CustomerUrlData(url=url),
            skip_diarization=True)

        return job.id

    def retrieve_transcript(self, job_id: int) -> Transcript | None:
        job_status = self._client.get_job_details(job_id).status
        if job_status == JobStatus.TRANSCRIBED:
            transcript_json = self._client.get_transcript_json(job_id)
            return Transcript.from_json(transcript_json)

        return None
