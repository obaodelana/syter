import json

from .rev_ai import Transcriber, Transcript


def main():
    option = int(input(
        "Would you like to\n(1) Parse a transcript\n(2) Generate a transcript\nOption: "))

    if option == 1:
        json_file = input("Path to JSON file: ")
        with open(json_file) as f:
            transcript = Transcript.from_json(json.load(f))
        for i in range(len(transcript)):
            print(f"[{i+1}] {transcript[i].text}")
    else:
        media_url = input("URL to media file: ")
        webhook_url = input("Webhook URL: ")

        transcriber = Transcriber("en", webhook_url)
        job_id = transcriber.submit_job(media_url)

        finished = input("Has the job finished? (y/n)")
        while finished.lower() != 'y':
            finished = input("Has the job finished? (y/n)")

        transcript = transcriber.retrieve_transcript(job_id)
        if transcript:
            print("Here's your transcript:")
            print(transcript)
        else:
            print("Failed to get transcript")


main()
