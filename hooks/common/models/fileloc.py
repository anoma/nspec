from pathlib import Path
from typing import Optional


class FileLoc:
    path: str
    _filepath: Path
    line: int
    column: int = 0
    text: Optional[str] = None

    def __init__(self, path: str, line: int, column: int, text: Optional[str] = None):
        self.path = path
        self._filepath = Path(path)
        self.line = line
        self.column = column
        self.text = text

    def filename(self) -> str:
        return self._filepath.name

    def set_filename(self, filename: str):
        self._filepath = self._filepath.with_name(filename)
        self.path = str(self._filepath)

    def __str__(self):
        msg = ""
        if self.text:
            msg = f"\n  {self.text}"

        return f"\033[91m{self.path}:{self.line}:{self.column}\033[0m" + msg
