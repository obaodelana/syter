class Resolution:
    def __init__(self, width: int = 0, height: int = 0, fps: int = 0):
        assert type(width) is int and width >= 0
        assert type(height) is int and height >= 0
        assert type(fps) is int and fps >= 0

        self.width = width
        self.height = height
        self.fps = fps
        self.is_audio = (fps == 0)

    @staticmethod
    def audio_only() -> "Resolution":
        return Resolution(0, 0, 0)

    def __str__(self) -> str:
        if self.fps > 0:
            return f"{self.height}p{self.fps}"
        return "audio only"

    def __eq__(self, other: "Resolution") -> bool:
        if self.is_audio and other.is_audio:
            return True
        else:
            return self.width == other.width and\
                self.height == other.height and\
                self.fps == other.fps

    def __lt__(self, other: "Resolution") -> bool:
        if self.height == other.height:
            return self.fps < other.fps
        return self.height < other.height
