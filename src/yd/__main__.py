from sys import argv

from main import YD
from models.file_extension import FileExtension


if __name__ == "__main__":
    link = ""
    if len(argv) > 1:
        link = argv[1]
    else:
        link = input("Video link: ")

    video = YD(link)
    formats = video.get_formats(
        extensions=[FileExtension.MP4, FileExtension.MP3, FileExtension.WAV, FileExtension.M4A])
    formats[0].id
    print(*formats, sep='\n')

    format_id = int(input("Choose a format: "))
    chosen_format = next(filter(lambda x: x.id == format_id, formats), None)
    if chosen_format:
        output_path = input("Download location: ")
        print("Downloading...")
        video.download(chosen_format, output_path)
        print("Done.")
    else:
        print("Invalid format id")
