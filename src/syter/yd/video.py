from pathlib import Path
from yt_dlp import YoutubeDL, DownloadError
from io import BytesIO
import subprocess

from models.video_format import VideoFormat
from models.file_extension import FileExtension
from models.resolution import Resolution
from models.file_size import FileSize


class Video:
    def __init__(self, link: str):
        assert type(link) is str

        self.link = link
        self.title: str | None = None
        self.description: str | None = None
        self.thumbnail_url: str | None = None
        self.formats: list[VideoFormat] | None = None

        self._get_video_details()
        if self.formats is None or len(self.formats) == 0:
            raise Exception("Invalid link provided.")

    def _get_video_details(self) -> None:
        with YoutubeDL() as yd:
            try:
                info_dict = yd.sanitize_info(
                    yd.extract_info(self.link, download=False))

                if info_dict.get("playlist_count") is not None:
                    raise Exception(
                        "The link provided is a playlist, not a video.")
                if "youtube" not in info_dict.get("extractor", ""):
                    raise Exception(
                        "The link provided is not to a YouTube video.")

                self.title = info_dict.get("title")
                self.description = info_dict.get("description")
                self.thumbnail_url = info_dict.get("thumbnail")
                self.link = info_dict.get("webpage_url", self.link)

                self._available_formats = VideoFormat.from_list(
                    info_dict.get("formats", []))
            except DownloadError as e:
                raise Exception(e.msg)

    @property
    def highest_quality_format(self) -> VideoFormat:
        return self.formats[-1]

    @property
    def lowest_quality_format(self) -> VideoFormat:
        return self.formats[0]

    def get_formats(self,
                    extensions: list[FileExtension] | None = None,
                    min_resolution: Resolution | None = None,
                    max_resolution: Resolution | None = None,
                    include_audio_only: bool = True,
                    include_video_only: bool = True,
                    max_file_size: FileSize | None = None) -> list[VideoFormat]:
        assert extensions is None or\
            type(extensions) is list
        assert min_resolution is None or\
            isinstance(min_resolution, Resolution)
        assert max_file_size is None or\
            isinstance(max_file_size, FileSize)
        assert type(include_audio_only) is bool

        if (extensions, min_resolution, max_resolution, max_file_size) ==\
                (None, None, None, None):
            return self.formats
        else:
            def _filter_func(f: VideoFormat) -> bool:
                if extensions is not None and f.file_extension not in extensions:
                    return False
                if min_resolution is not None and\
                    (f.resolution.fps, f.resolution.width, f.resolution.height) <\
                        (min_resolution.fps, min_resolution.width, min_resolution.height):
                    return False
                if max_resolution is not None and\
                    (f.resolution.fps, f.resolution.width, f.resolution.height) >\
                        (max_resolution.fps, max_resolution.width, max_resolution.height):
                    return False
                if not include_audio_only and f.resolution.is_audio_only:
                    return False
                if not include_video_only and f.resolution.is_video_only:
                    return False
                if max_file_size is not None and\
                        (f.file_size.B == 0 or f.file_size > max_file_size):
                    return False

                return True

            desired_formats = list(filter(_filter_func, self.formats))
            return desired_formats

    def download(self,
                 format: VideoFormat | None = None,
                 output_path: str | None = None,
                 extract_audio: bool = False) -> bool:
        assert format is None or isinstance(format, VideoFormat)
        assert output_path is None or type(output_path) is str
        assert type(extract_audio) is bool

        if format is None:
            format = self.lowest_quality_format

        if output_path is not None:
            p = Path(output_path).absolute()
        else:
            p = Path.cwd()

        options = {
            "quiet": True,
            "format": str(format.id),
            "keepvideo": True,
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav"
            },] if extract_audio else [],
            # If `p` is a directory, put inside directory and store as video title
            "outtmpl": (f"{p}/%(title)s.%(ext)s" if p.is_dir()
                        else str(p))
        }
        with YoutubeDL(options) as yd:
            try:
                return_code = yd.download([self.link])
            except DownloadError as e:
                raise Exception(e.msg)

        return return_code == 0

    def open(self, format: VideoFormat | None = None) -> BytesIO | None:
        assert format is None or isinstance(format, VideoFormat)

        if format is None:
            format = self.lowest_quality_format

        args = ["yt-dlp",
                "-q",
                "--no-playlist",
                "-f", str(format.id),
                "-o", "-",
                self.link]
        try:
            yd = subprocess.run(args, capture_output=True)
            return BytesIO(yd.stdout)
        except subprocess.CalledProcessError:
            return None

    def __str__(self) -> str:
        f"{self.title} ({self.link})"

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "format_count": len(self.formats),
            "thumbnail_url": self.thumbnail_url
        }
