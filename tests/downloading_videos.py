from os import path
from youtube_dl import YoutubeDL
import json


class MyLogger(object):
    def debug(self, msg):
        with open("log.json", "w") as j:
            print(msg, file=j)
            print("called")
        # json.loads(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download_video(link: str):
    file_path = path.realpath(__file__)
    directory = path.join(path.dirname(file_path), "test_videos")

    options = {
        "simulate": True,
        "dump_single_json": True,
        "forcejson": True,
        # "listformats": True,
        "format": "best[height<=360][ext=mp4]",
        "postprocessors": [{"key": "FFmpegExtractAudio"}],
        "keepvideo": True,
        "quiet": True,
        "outtmpl": f"{directory}/%(id)s/%(id)s.%(ext)s",
        "logger": MyLogger()
    }

    with YoutubeDL(options) as yd:
        yd.download([link])


download_video("https://www.youtube.com/watch?v=A227PUD6Z9Y")
