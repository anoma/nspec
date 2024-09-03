import json
from typing import Dict


class ResultEntry:
    file: str
    index: int
    matches: Dict[str, int]
    url: str

    def __init__(self, file: str, index: int, matches: Dict[str, int], url):
        self.file = file
        self.index = index
        self.matches = matches
        self.url = url

    @property
    def text(self):
        if self.file:
            return self.file
        return self.index

    def __repr__(self):
        return f"""
        ResultEntry:
            File: {self.file}
            Index: {self.index}
            Matches: {self.matches}
            url: {self.url}
        """

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def to_dict(self):
        return {
            "file": self.file,
            "index": self.index,
            "matches": self.matches,
            "url": self.url,
        }
