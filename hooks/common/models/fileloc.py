from typing import Optional


class FileLoc:
    path: str
    line: int
    column: int = 0
    message: Optional[str] = None

    def __init__(
        self, path: str, line: int, column: int, message: Optional[str] = None
    ):
        self.path = path
        self.line = line
        self.column = column
        self.message = message

    def __str__(self):
        # print the path in red
        return f"\033[91m{self.path}:{self.line}:{self.column}\033[0m\n  {self.message or ''}"
