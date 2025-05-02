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

            return sorted(formats, key=lambda f: (f.file_size.B if f.file_size.B != 0
                                                  else float("inf"),
                                                  f.resolution))
        except json.JSONDecodeError:
            return []
