import os
from openai import OpenAI
from inspect import getdoc

from .models.key_moment import KeyMoment


class KeyMomentExtractor:
    def __init__(self) -> None:
        self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4.1-nano"

    def extract(self,
                title: str,
                description: str,
                transcript: list[str]) -> list[KeyMoment]:
        """
        # Identity

        You are a content creator's assistant. Your job is to help extract key moments from a long-form video to create multiple short videos that are 5-90 seconds long. Examples of key moments are emotional, informative, funny or climatic moments.

        # Input

        You will receive
        - The video title
        - The video description
        - A list of transcribed sentences that make up the video. Each sentence is numbered and starts on a new line

        ## Input format

        Title: "Finish Work Faster by Copying How Olympic Athletes Train"
        Description: "Here I describe a technique for getting more work done, pulled from how Olympic athletes train."
        Transcript:
        [1] In  this  video,  I'm  gonna  share  you  a  trick  pulled  from  the  way  Olympic  athletes  train  as  a  way  to  finish  more  work  in  less  time.
        [2] But  the  idea  in  the  book  was  that  Olympic  athletes  do  not  train  nonstop.

        # Output

        If the transcript is incoherent or unintelligible, respond by saying "I don't understand this."

        Otherwise, respond by specifying the sentence numbers of the parts of the video to be included in a particular short and a concise caption that accompanies the short. Each short should be in a single line.

        ## Output format

        [1,3] caption text for short 1
        [2,4,6,7,9,10] caption text for short 2

        # Instructions

        - The caption text should be brief and catchy summary that highlights the key moment. Go for a viral TikTok-like caption that is both informational and trendy. Use the video title and description for context when generating captions. 
        - Aim to generate about 3-10 shorts.
        - Ensure each short has proper context. Try to include sentences that provide appropriate background information for the key moment.
        - Prioritize longer shorts that tell a story over generating a large number of shorts.
        """

        assert type(title) is str
        assert type(description) is str
        assert type(transcript) is list

        user_prompt = f'Title: "{title}"\nDescription: "{description}"\n'
        for i, sentence in enumerate(transcript, start=1):
            user_prompt += f"[{i}] {sentence}"
            if i < len(transcript):
                user_prompt += '\n'

        response = self._client.responses.create(
            instructions=getdoc(self.extract),
            model=self.model,
            temperature=1.0,
            max_output_tokens=1024,
            input=user_prompt
        )

        model_output = response.output_text
        lines = model_output.split("\n")

        return [KeyMoment(line) for line in lines]
