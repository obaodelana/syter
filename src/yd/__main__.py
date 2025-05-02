from youtube_downloader import YD


if __name__ == "__main__":
    video = YD("https://www.youtube.com/watch?v=MiNaManmFQU")
    # print(*video.get_formats("mp4"), sep="\n")

    # video.download(output_path="/Users/obaodelana/Desktop/yt")
