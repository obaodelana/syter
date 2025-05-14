class KeyMoment:
    def __init__(self, text: str) -> None:
        """
        Expecting format: "[1,3] caption"
        """

        starting_bracket = text.index("[")
        ending_bracket = text.index("]")

        self.segments = list(map(
            lambda i: int(i),
            text[starting_bracket+1:ending_bracket].split(",")
        ))
        self.caption = text[ending_bracket+1:].strip()

    def __str__(self) -> str:
        return f"{", ".join(self.segments)} {self.caption}"
