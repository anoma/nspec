import os
from typing import Dict, Optional
from urllib.parse import urljoin

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.utils import get_markdown_title


def fix_site_url(config: MkDocsConfig) -> MkDocsConfig:
    version = os.environ.get("MIKE_DOCS_VERSION", "")
    config["docs_version"] = version
    if version and "site_url" in config and config.get("site_url"):
        if config["canonical_version"] is not None:
            version = config["canonical_version"]
        config["site_url"] = urljoin(config["site_url"], version)
    return config


def get_page_title(page_src: str, meta_data: dict) -> Optional[str]:
    """Returns the title of the page. The title in the meta data section
    will take precedence over the H1 markdown title if both are provided."""
    return (
        meta_data["title"]
        if "title" in meta_data and isinstance(meta_data["title"], str)
        else get_markdown_title(page_src)
    )
