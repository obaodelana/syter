from sys import argv

from youtube_downloader import YD
from models.file_extension import FileExtension
from models.resolution import Resolution


if __name__ == "__main__":
    link = ""
    if len(argv) > 1:
        link = argv[1]
    else:
        link = input("Video link: ")

    video = YD(link)
    available_formats = video.get_formats(
        extensions=[FileExtension.MP3, FileExtension.M4A, FileExtension.WAV],
        # min_resolution=Resolution(fps=30)
    )
    print(*available_formats, sep="\n")
    if len(available_formats) != 0:
        video.download(output_path="~/Downloads/music/QT2",
                       format=available_formats[0],
                       print_progress=True)
    else:
        print("No audio files available.")
