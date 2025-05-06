import unittest
from yd.models.video_time import VideoTime


class TestPrinting(unittest.TestCase):
    def test_print_ms(self):
        one_second = VideoTime(ms=1000)

        assert str(one_second) == "00:00:01:00"


if __name__ == "__main__":
    unittest.main()
