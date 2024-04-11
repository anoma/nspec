from typing import Optional
from mkdocs.utils import get_markdown_title


def fix_url(root: str, url: str, html: bool = False, ROOT_URL="/nspec/") -> str:
    if url.startswith("http"):
        return url
    right_url = url.lstrip(".").lstrip("/")
    _root = root
    if _root.endswith(ROOT_URL):
        _root = root.rstrip("/")
    if html:
        right_url = right_url.replace(".md", ".html")
    return _root + "/" + right_url


def get_page_title(page_src: str, meta_data: dict) -> Optional[str]:
    """Returns the title of the page. The title in the meta data section
    will take precedence over the H1 markdown title if both are provided."""
    return (
        meta_data["title"]
        if "title" in meta_data and isinstance(meta_data["title"], str)
        else get_markdown_title(page_src)
    )
