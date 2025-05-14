class YDLogger:
    def __init__(self) -> None:
        self._debug_log: list[str] = []
        self._warning_log: list[str] = []
        self._error_log: list[str] = []

    def debug(self, msg: str) -> None:
        self._debug_log.append(msg)

    def warning(self, msg: str) -> None:
        self._warning_log.append(msg)

    def error(self, msg: str) -> None:
        self._error_log.append(msg)

    @property
    def debug_log(self) -> list[str]:
        return self._debug_log

    @property
    def warning_log(self) -> list[str]:
        return self._warning_log

    @property
    def error_log(self) -> list[str]:
        return self._error_log
