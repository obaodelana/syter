class VideoDuration:
    def __init__(self, duration_str: str) -> None:
        assert type(duration_str) is str

        self.seconds = 0
        self.minutes = 0
        self.hours = 0

        current_number = ""
        for char in duration_str:
            # Accumulate number
            if char.isnumeric():
                current_number += char
            elif len(current_number) > 0:
                number = int(current_number)
                current_number = ""
                match char:
                    case "H":
                        self.hours = number
                    case "M":
                        self.minutes = number
                    case "S":
                        self.seconds = number

        assert current_number == "", "Something went wrong with the parsing"

    def __str__(self) -> str:
        string = ""
        if self.hours > 0:
            string = f"{self.hours:02d}:"
        string += f"{self.minutes:02d}:{self.seconds:02d}"

        return string
