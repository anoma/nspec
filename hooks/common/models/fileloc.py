from typing import Optional


class FileLoc:
    path: str
    line: int
    column: int = 0
    text: Optional[str] = None

    def __init__(self, path: str, line: int, column: int, text: Optional[str] = None):
        self.path = path
        self.line = line
        self.column = column
        self.text = text

    def __str__(self):
        msg = ""
        if self.text:
            msg = f"\n  {self.text}"

        return f"\033[91m{self.path}:{self.line}:{self.column}\033[0m" + msg
