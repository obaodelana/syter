# Syter

>[!NOTE]
> Work in progress.

I'm building an API that automates the process of extracting shorts from a video.

## Pipeline
1. Download YouTube video: It uses [yt-dlp](https://github.com/yt-dlp/yt-dlp/) to download a low quality audio-only version of the YouTube video.
2. Transcribe video: It uses [Reverb Turbo's](https://www.rev.ai/) transcription model to transcribe the video word for word. I collate the transcribed words as sentences, and pass it to the next stage.
3. Extract key moments: Each sentence is numbered and passed to OpenAI's [GPT-4.1 nano](https://platform.openai.com/docs/models/gpt-4.1-nano) model with a prompt asking it to choose a bunch of sentences that make up a single short.
4. Display and download: The timestamps of each returned sentence is retrieved, then I call [yt-dlp](https://github.com/yt-dlp/yt-dlp/) again to download high-quality videos of the specified segments. (At first, I wanted to allow the user edit the shorts directly in the browser, but I'll do that later 🤞🏾.)

## Purpose
In this way, video editing time is cut down by removing the process of pinpointing the most meaningful segments to include in a short. Syter allows the video editor to mass create shorts because the only work done now is merging and adding finishing touches.

---

Once the API and front end is done, I'll paste the link here.
