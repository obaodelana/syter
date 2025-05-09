from .sentence import Sentence
from .transcript_time import TranscriptTime


class Transcript:
    def __init__(self, sentences: list[Sentence]) -> None:
        assert type(sentences) is list
        assert len(sentences) > 0

        self._sentences = sentences

    @property
    def start_time(self) -> TranscriptTime:
        return self._sentences[0].start_time

    @property
    def end_time(self) -> TranscriptTime:
        return self._sentences[-1].end_time

    @property
    def duration(self) -> float:
        return (self.end_time - self.start_time).value

    @property
    def text(self) -> str:
        return "\n".join([s.text for s in self._sentences])

    def __len__(self) -> int:
        return len(self._sentences)

    def __getitem__(self, index: int) -> Sentence:
        if index < 0 or index >= len(self):
            raise IndexError()
        return self._sentences[index]

    def __str__(self) -> str:
        return "\n".join([str(s) for s in self._sentences])
