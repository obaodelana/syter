from models.word import Word
from models.sentence import Sentence
from models.transcript import Transcript

if __name__ == "__main__":
    dummy_transcript = Transcript([
        Sentence([
            Word(0.305, 0.525, "In"),
            Word(0.525, 0.685, "this"),
            Word(0.685, 0.885, "video"),
        ]),
        Sentence([
            Word(42.425, 42.645, "But"),
            Word(42.785, 43.005, "the"),
            Word(43.005, 43.245, "goal"),
        ]),
        Sentence([
            Word(142.185, 142.465, "it's"),
            Word(142.465, 142.625, "fairly"),
            Word(142.695, 142.985, "easy"),
        ])
    ])

    print(dummy_transcript)
