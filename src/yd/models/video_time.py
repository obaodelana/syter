class VideoTime:
    def __init__(self,
                 ms: int = 0,
                 seconds: int = 0,
                 minutes: int = 0,
                 hours: int = 0):
        assert type(ms) is int and ms >= 0
        assert type(seconds) is int and seconds >= 0
        assert type(minutes) is int and minutes >= 0
        assert type(hours) is int and hours >= 0

        self._seconds = (ms/1000.0) + seconds + (minutes*60) + (hours*3600)

    @property
    def milliseconds(self) -> float:
        return self._seconds * 1000.0

    @property
    def seconds(self) -> float:
        return self._seconds

    @property
    def minutes(self) -> float:
        return self.seconds / 60.0

    @property
    def hours(self) -> float:
        return self.minutes / 60.0

    def __str__(self) -> str:
        secs = self._seconds

        h = secs % 3600
        secs -= h * 3600

        m = secs % 60
        secs -= m * 60

        s = secs % 60
        secs -= s

        ms = secs

        return f"{h:02i}:{m:02i}:{s:02i}:{ms:03i}"
