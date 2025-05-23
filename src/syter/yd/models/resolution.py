class Resolution:
    def __init__(self,
                 width: int = 0,
                 height: int = 0,
                 fps: int = 0,
                 audio_channels: int = 0):
        assert type(width) is int and width >= 0
        assert type(height) is int and height >= 0
        assert type(fps) is int and fps >= 0
        assert type(audio_channels) is int and audio_channels >= 0

        self.width = width
        self.height = height
        self.fps = fps
        self.audio_channels = audio_channels
        self.is_audio_only = (fps == 0)
        self.is_video_only = (audio_channels == 0)

    def get_format_string(self, comparison_operator="=") -> str:
        assert type(comparison_operator) is str\
            and 1 <= len(comparison_operator) <= 2

        format_string = ""
        if self.width > 0:
            format_string += f"[width{comparison_operator}{self.width}]"
        if self.height > 0:
            format_string += f"[height{comparison_operator}{self.height}]"
        if self.fps > 0:
            format_string += f"[fps{comparison_operator}{self.fps}]"

        return format_string

    def __str__(self) -> str:
        if not self.is_audio_only:
            string = f"{self.height}p{self.fps}"
            if self.is_video_only:
                string += " (video only)"
            return string
        return "audio only"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Resolution):
            return False
        elif self.is_audio_only and other.is_audio_only:
            return True
        else:
            return self.width == other.width and\
                self.height == other.height and\
                self.fps == other.fps

    def __lt__(self, other: "Resolution") -> bool:
        if self.height == other.height:
            return self.fps < other.fps
        return self.height < other.height
