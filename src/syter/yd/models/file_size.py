class FileSize:
    def __init__(self, size: int):
        self._size_in_bytes = size

    @property
    def B(self) -> int:
        return self._size_in_bytes

    @property
    def KB(self) -> float:
        return self.B / 1024.0

    @property
    def MB(self) -> float:
        return self.KB / 1024.0

    @property
    def GB(self) -> float:
        return self.MB / 1024.0

    def __str__(self) -> str:
        if self.B == 0:
            return "not specified"
        elif self.KB < 0.1:
            return f"{self.B:.2f} B"
        elif self.MB < 0.1:
            return f"{self.KB:.2f} KB"
        elif self.GB < 0.1:
            return f"{self.MB:.2f} MB"
        else:
            return f"{self.GB:.2f} GB"

    def __eq__(self, other: "FileSize") -> bool:
        return self.B == other.B

    def __lt__(self, other: "FileSize") -> bool:
        return self.B < other.B

    def __gt__(self, other: "FileSize") -> bool:
        return self.B > other.B
