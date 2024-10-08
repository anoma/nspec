import logging
from typing import Optional

from .loc import FileLoc

log: logging.Logger = logging.getLogger("mkdocs")


class WikiLink:
    def __init__(
        self,
        page: str,
        hint: Optional[str] = None,
        anchor: Optional[str] = None,
        display: Optional[str] = None,
        loc: Optional[FileLoc] = None,
    ):
        self.page: str = page.strip()
        self.hint: Optional[str] = hint.strip() if hint else None
        self.anchor: Optional[str] = anchor.strip() if anchor else None
        self.display: Optional[str] = display.strip() if display else None
        self.loc: Optional[FileLoc] = loc

    def __hash__(self):
        return hash(self.page)

    @property
    def text(self):
        if self.display:
            return self.display
        return self.page

    def __repr__(self):
        return f"""
    WikiLink:
      Page: {self.page}
      {'Hint: ' + self.hint if self.hint else ''}
      {'Anchor: ' + self.anchor if self.anchor else ''}
      {'Display: ' + self.display if self.display else ''}
      {'Loc: ' + str(self.loc) if self.loc else ''}
    """
