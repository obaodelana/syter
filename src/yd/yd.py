from youtube_dl import YoutubeDL
from models.video_format import VideoFormat
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
            yd.download([self._link])
            if len(yd_logger.error_log) != 0:
                raise Exception(yd_logger.error_log[0])

        # JSON is always the last message printed
        json_content = yd_logger.debug_log[-1]

        return VideoFormat.from_json(json_content)

    @property
    def formats(self) -> list[VideoFormat]:
        return self._available_formats

    @property
    def highest_quality_format(self) -> VideoFormat:
        return self._available_formats[-1]

    @property
    def lowest_quality_format(self) -> VideoFormat:
        return self._available_formats[0]
