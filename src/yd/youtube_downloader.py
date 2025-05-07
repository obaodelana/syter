from pathlib import Path
from yt_dlp import YoutubeDL

from models.video_format import VideoFormat
from models.file_extension import FileExtension
from models.resolution import Resolution
from models.file_size import FileSize


class YD:
    def __init__(self, link: str):
        assert type(link) is str

        self._link = link
        self._available_formats = self._get_available_formats()

        if len(self._available_formats) == 0:
            raise Exception("This video is invalid")

    def _get_available_formats(self) -> list[VideoFormat]:
        options = {
            "simulate": True,
            "quiet": True,
            "dump_single_json": True,
        }
        with YoutubeDL(options) as yd:
            info_dict: dict = yd.sanitize_info(
                yd.extract_info(self._link, download=False))
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

    def get_formats(self,
                    extensions: list[FileExtension] | None = None,
                    min_resolution: Resolution | None = None,
                    max_resolution: Resolution | None = None,
                    include_audio: bool = True,
                    max_file_size: FileSize | None = None) -> list[VideoFormat]:
        assert extensions is None or\
            type(extensions) is list
        assert min_resolution is None or\
            isinstance(min_resolution, Resolution)
        assert max_file_size is None or\
            isinstance(max_file_size, FileSize)
        assert type(include_audio) is bool

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
                if not include_audio and f.resolution == Resolution.audio_only():
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
                 extract_audio: bool = False,
                 print_progress: bool = False) -> bool:
        assert format is None or isinstance(format, VideoFormat)
        assert output_path is None or type(output_path) is str
        assert type(extract_audio) is bool
        assert type(print_progress) is bool

        if format is None:
            format = self.lowest_quality_format

        if output_path is not None:
            p = Path(output_path).absolute()
        else:
            p = Path.cwd()

        def progress_hook(info: dict) -> None:
            # They already do the printing
            if info["status"] == "downloading":
                pass
            elif info["status"] == "finished":
                print("\nDone downloading.")

        options = {
            "quiet": True,
            "format": str(format.id),
            "progress_hooks": [progress_hook] if print_progress else [],
            "keepvideo": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav"
            },] if extract_audio else [],
            # If `p` is a directory, put inside directory and store as video title
            "outtmpl": (f"{p}/%(title)s.%(ext)s" if p.is_dir() or str(p).endswith("/")
                        else str(p))
        }
        with YoutubeDL(options) as yd:
            return_code = yd.download([self._link])

        return return_code
