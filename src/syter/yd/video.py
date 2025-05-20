from io import BytesIO
import subprocess

from .models.file_extension import FileExtension
from .models.resolution import Resolution
from .models.file_size import FileSize
from .models.video_duration import VideoDuration

# TODO: Define custom exception type for errors


class Video:
    def __init__(self,
                 id: str,
                 duration: VideoDuration):
        assert type(id) is str
        assert isinstance(duration, VideoDuration)

        self.id = id
        self.duration = duration

    @property
    def link(self):
        return f"https://www.youtube.com/watch?v={self.id}"

    # TODO: Test
    def open(self,
             min_resolution: Resolution | None = None,
             max_resolution: Resolution | None = None,
             file_extensions: list[FileExtension] | None = None,
             max_file_size: FileSize | None = None) -> BytesIO:
        assert min_resolution is None or isinstance(min_resolution, Resolution)
        assert max_resolution is None or isinstance(max_resolution, Resolution)
        assert file_extensions is None or type(file_extensions) is list

        format_string = ""
        if min_resolution is not None:
            format_string += min_resolution.get_format_string("<=")
        if max_resolution is not None:
            format_string += max_resolution.get_format_string(">=")
        if file_extensions is not None:
            for ext in file_extensions:
                format_string += f"[ext={ext}]"
        if max_file_size is not None:
            format_string += f"[filesize<={max_file_size.MB:d}M]"

        args = ["yt-dlp",
                "-q",  # Quiet
                "-f", format_string,
                # Sort formats by size and bit rate
                "-S", "+size,+br"
                # When (1) is chosen, output merged video as mp4
                "--merge-output-format", "mp4",
                "-o", "-",
                "-N", "3",  # Use 3 threads
                self.id]

        try:
            yd = subprocess.run(args, capture_output=True)
        except subprocess.CalledProcessError:
            raise Exception()

        return BytesIO(yd.stdout)

    def open_audio(self) -> BytesIO:
        """
        Download the lowest quality audio file to a buffer in memory.
        """
        args = ["yt-dlp",
                "-q",  # Quiet
                "-f", "ba",  # Best audio format
                # Sort formats by size, bit rate and extension
                "-S", "+size,+br,+aext"
                "-o", "-",
                "-N", "3",  # Use 3 threads
                self.id]

        try:
            yd = subprocess.run(args, capture_output=True)
        except subprocess.CalledProcessError:
            raise Exception()
        return BytesIO(yd.stdout)

    def __str__(self) -> str:
        return str({
            "id": self.id,
            "duration": str(self.duration)
        })
