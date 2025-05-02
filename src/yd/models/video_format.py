import json

from .file_extension import FileExtension
from .resolution import Resolution
from .file_size import FileSize


class VideoFormat:
    def __init__(self,
                 format_id: int,
                 resolution: Resolution,
                 file_extension: FileExtension,
                 file_size: FileSize):
        self.id = format_id
        self.resolution = resolution
        self.file_extension = file_extension
        self.file_size = file_size

    def __str__(self) -> str:
        return f"{self.id} (.{self.file_extension}): {self.resolution} ({self.file_size})"

    def __repr__(self) -> str:
        return str(self)

    def __lt__(self, other: "VideoFormat") -> bool:
        if self.file_size.B != 0 and other.file_size.B != 0:
            return self.file_size < other.file_size
        else:
            return self.resolution < other.resolution

    @staticmethod
    def from_json(json_content: str) -> list["VideoFormat"]:
        assert type(json_content) is str, "Only give me json as a string"

        def as_video_format(dct: dict) -> dict | VideoFormat:
            if "format_id" in dct and "title" not in dct:
                return VideoFormat(
                    dct["format_id"],
                    Resolution(dct.get("width", 0),
                               dct.get("height", 0),
                               dct.get("fps", 0)),
                    FileExtension(dct.get("ext")),
                    FileSize(dct.get("filesize", 0))
                )
            return dct

        try:
            json_dict = json.loads(json_content, object_hook=as_video_format)
            formats: list[VideoFormat] = json_dict["formats"]
            return sorted(formats)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def from_dict(dct: dict) -> list["VideoFormat"]:
        assert type(dct) is dict

        def _get_int(val) -> int:
            try:
                integer = int(val)
                return integer
            except:
                return 0

        formats: list[VideoFormat] = []
        for raw_format in dct.get("formats", []):
            if "format_id" in raw_format:
                id = _get_int(raw_format["format_id"])
                if id == 0:  # Ids should be numbers
                    continue
                width = _get_int(raw_format.get("width", 0))
                height = _get_int(raw_format.get("width", 0))
                fps = _get_int(raw_format.get("fps", 0))
                file_extension = raw_format.get("ext")
                if file_extension not in FileExtension.__members__.values():
                    continue
                file_size = _get_int(raw_format.get("filesize",
                                                    raw_format.get("filesize_approx", 0)))

                formats.append(VideoFormat(
                    id,
                    Resolution(width, height, fps),
                    FileExtension(file_extension),
                    FileSize(file_size)
                ))

        return formats
