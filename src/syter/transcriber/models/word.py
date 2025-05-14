from .transcript_time import TranscriptTime


class Word:
    def __init__(self,
                 start_time: float,
                 end_time: float,
                 text: str) -> None:
        assert type(start_time) is float
        assert type(end_time) is float and end_time >= start_time
        assert type(text) is str

        self.start_time = TranscriptTime(start_time)
        self.end_time = TranscriptTime(end_time)
        self.text = text

    @property
    def length(self) -> float:
        return (self.end_time - self.start_time).value

    def __str__(self) -> str:
        return self.text
