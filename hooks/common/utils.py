from typing import Optional

from mkdocs.utils import get_markdown_title


def fix_url(url: str, use_html_ext: bool = False, root: str = "/nspec/") -> str:
    if url.startswith("http"):
        return url

    right_url = url.lstrip(".").lstrip("/")
    if use_html_ext:
        right_url = right_url.replace(".md", ".html")

    return root.rstrip("/") + "/" + right_url


def get_page_title(page_src: str, meta_data: dict) -> Optional[str]:
    """Returns the title of the page. The title in the meta data section
    will take precedence over the H1 markdown title if both are provided."""
    return (
        meta_data["title"]
        if "title" in meta_data and isinstance(meta_data["title"], str)
        else get_markdown_title(page_src)
    )
