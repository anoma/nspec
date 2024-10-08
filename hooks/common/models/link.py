from typing import Optional

from .loc import FileLoc


class Link:
    def __init__(
        self,
        display: Optional[str] = None,
        anchor: Optional[str] = None,
        url: Optional[str] = None,
        fileloc: Optional[FileLoc] = None,
    ):
        self.anchor: Optional[str] = anchor.strip() if anchor else None
        self.display: Optional[str] = display.strip() if display else None
        self.url: Optional[str] = url.strip() if url else None
        self.fileloc: Optional[FileLoc] = fileloc

    @property
    def text(self):
        if self.display:
            return self.display
        return self.url

    def __repr__(self):
        return f"""
    Link:
        {'Display: ' + self.display if self.display else ''}
        {'Anchor: ' + self.anchor if self.anchor else ''}
        {'URL: ' + self.url if self.url else ''}
        {'FileLoc: ' + str(self.fileloc) if self.fileloc else ''}
    """
