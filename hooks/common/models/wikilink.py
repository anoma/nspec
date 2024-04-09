from typing import Optional


class WikiLink:

    def __init__(
        self,
        page: str,
        hint: Optional[str] = None,
        anchor: Optional[str] = None,
        display: Optional[str] = None,
    ):
        self.page: str = page.strip()
        self.hint: Optional[str] = hint.strip() if hint else None
        self.anchor: Optional[str] = anchor.strip() if anchor else None
        self.display: Optional[str] = display.strip() if display else None

    def __hash__(self):
        return hash(self.page)

    @property
    def text(self):
        if self.display:
            return self.display
        return self.page

    def __repr__(self):
        s = f"page={self.page}, "
        if self.hint:
            s += f"hint={self.hint}, "
        if self.anchor:
            s += f"anchor={self.anchor}, "
        if self.display:
            s += f"display={self.display}"
        return f"WikiLink({s})"
