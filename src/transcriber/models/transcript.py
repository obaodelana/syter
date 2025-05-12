from .word import Word
from .sentence import Sentence
from .transcript_time import TranscriptTime


class Transcript:
    def __init__(self, sentences: list[Sentence]) -> None:
        assert type(sentences) is list
        assert len(sentences) > 0

        self._sentences = sentences

    @classmethod
    def from_json(cls, json_dict: dict) -> "Transcript":
        assert type(json_dict) is dict
        assert "monologues" in json_dict, "JSON is not a RevAI response"

        word_list: list[Word] = []
        sentences: list[Sentence] = []
        for monologue in json_dict["monologues"]:
            for element in monologue["elements"]:
                if element["type"] == "text":
                    word_list.append(Word(
                        float(element["ts"]),
                        float(element["end_ts"]),
                        element["value"]
                    ))
                elif element["type"] == "punct":
                    punctuation = element["value"]
                    if len(word_list) > 0:
                        # Add punctuation to last word
                        word_list[-1].text += punctuation
                        # Full stop denotes sentence end
                        if punctuation == ".":
                            sentences.append(Sentence(word_list.copy()))
                            word_list.clear()

        # If world list is not empty, then there's a remaining sentence
        if len(word_list) > 0:
            sentences.append(Sentence(word_list.copy()))

        return cls(sentences)

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
