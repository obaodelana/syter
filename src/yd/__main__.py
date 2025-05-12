from sys import argv

from main import YD
from models.file_extension import FileExtension
from models.resolution import Resolution


if __name__ == "__main__":
    link = ""
    if len(argv) > 1:
        link = argv[1]
    else:
        link = input("Video link: ")

    video = YD(link)
