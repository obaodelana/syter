from .transcript_time import TranscriptTime
from .word import Word


class Sentence:
    def __init__(self, words: list[Word]) -> None:
        assert type(words) is list
        assert len(words) > 0

        self._words = words

    @property
    def start_time(self) -> TranscriptTime:
        return self._words[0].start_time

    @property
    def end_time(self) -> TranscriptTime:
        return self._words[-1].end_time

    @property
    def duration(self) -> float:
        return (self.end_time - self.start_time).value

    @property
    def text(self) -> str:
        return " ".join(self._words)

    def __str__(self) -> str:
        return f"[${self.start_time}-{self.end_time}] {self.text}"
