from video_time import VideoTime


class Duration:
    def __init__(self,
                 start_time: VideoTime,
                 end_time: VideoTime | None = None):
        assert isinstance(start_time, VideoTime)
        assert end_time is None or isinstance(end_time, VideoTime)
