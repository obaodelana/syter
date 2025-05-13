from main import Transcriber


def main():
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
