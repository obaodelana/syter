class TranscriptTime:
    def __init__(self, seconds: float) -> None:
        assert type(seconds) is float

        self.value = seconds

    def __sub__(self, other: "TranscriptTime") -> "TranscriptTime":
        return TranscriptTime(self.value - other.value)

    def __str__(self) -> str:
        s = self.value

        hours = s // 3600.0
        s -= hours * 3600

        minutes = s // 60.0
        s -= minutes * 60

        seconds = int(s)

        string = f"{minutes:02i}:{seconds:02i}"
        if hours > 0:
            string = f"{hours:02i}:" + string

        return string
