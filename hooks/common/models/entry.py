import json
from typing import Dict, List


class ResultEntry:
    file: str
    index: int
    matches: List[Dict[str, int]]
    url: str
    name: str

    def __init__(
        self, file: str, index: int, matches: List[Dict[str, int]], url: str, name: str
    ):
        self.file = file
        self.index = index
        self.matches = matches
        self.url = url
        self.name = name

    @property
    def text(self):
        if self.name:
            return self.name
        if self.file:
            return self.file
        return self.index

    def __repr__(self):
        return f"""
        ResultEntry:
            File: {self.file}
            Name: {self.name}
            Index: {self.index}
            Matches: {self.matches}
            url: {self.url}
        """

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def to_dict(self):
        return {
            "file": self.file,
            "index": self.index,
            "matches": self.matches,
            "url": self.url,
            "name": self.name,
        }
