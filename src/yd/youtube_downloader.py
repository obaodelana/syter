from pathlib import Path
from yt_dlp import YoutubeDL

from models.video_format import VideoFormat
from models.file_extension import FileExtension
from util.yd_logger import YDLogger

# TODO: Download function
# TODO: Stream function


class YD:
    def __init__(self, link: str):
        assert type(link) is str

        self._link = link
        self._available_formats = self._get_available_formats()

        if len(self._available_formats) == 0:
            raise Exception("This video is invalid")

    def _get_available_formats(self) -> list["VideoFormat"]:
        yd_logger = YDLogger()
        options = {
            "simulate": True,
            "quiet": True,
            "dump_single_json": True,
            "logger": yd_logger
        }
        with YoutubeDL(options) as yd:
            info_dict: dict = yd.extract_info(self._link, download=False)
            return VideoFormat.from_dict(info_dict)

    @property
    def formats(self) -> list[VideoFormat]:
        return self._available_formats

    @property
    def highest_quality_format(self) -> VideoFormat:
        return self._available_formats[-1]

    @property
    def lowest_quality_format(self) -> VideoFormat:
        return self._available_formats[0]

    def get_formats(self, extension: FileExtension | str | None) -> list[VideoFormat]:
        assert extension is None\
            or type(extension) is str or isinstance(extension, FileExtension)

        if type(extension) is str:
            extension = FileExtension(extension)

        if extension is None:
            return self.formats
        else:
            desired_formats = [f for f in self.formats
                               if f.file_extension == extension]
            return desired_formats

    def download(self,
                 format: VideoFormat | None = None,
                 output_path: str | None = None) -> bool:
        assert format is None or isinstance(format, VideoFormat)
        assert output_path is None or type(output_path) is str

        if format is None:
            format = self.lowest_quality_format

        if output_path is not None:
            p = Path(output_path).absolute()
        else:
            p = Path.cwd()

        logger = YDLogger()
        options = {
            "quiet": True,
            "logger": logger,
            "format": format.id,
            # If `p` is a directory, put inside directory and store as video title
            "outtmpl": (f"{p}/%(title)s.%(ext)s" if p.is_dir() or "/" in str(p)
                        else str(p))
        }
        with YoutubeDL(options) as yd:
            yd.download([self._link])

        return len(logger.error_log) == 0  # Successful means no errors
