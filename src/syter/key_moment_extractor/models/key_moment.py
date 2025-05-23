class KeyMoment:
    def __init__(self, text: str) -> None:
        """
        Expecting format: "[1,3] caption"
        """

        starting_bracket = text.index("[")
        ending_bracket = text.index("]")

        self._segments = text[starting_bracket+1:ending_bracket].split(",")
        self.caption = text[ending_bracket+1:].strip()

    @property
    def segments(self):
        return list(map(int, self._segments))

    def __str__(self) -> str:
        return f"[{",".join(self._segments)}] {self.caption}"
