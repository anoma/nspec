import logging
import os
from typing import Dict, Optional
from urllib.parse import urljoin

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.utils import get_markdown_title

log = logging.getLogger("mkdocs")


def fix_site_url(config: MkDocsConfig) -> MkDocsConfig:

    if os.environ.get("SITE_URL"):
        config["site_url"] = os.environ["SITE_URL"]
        if not config["site_url"].endswith("/"):
            config["site_url"] += "/"
        log.info("Using SITE_URL environment variable: %s", os.environ["SITE_URL"])
        return config

    log.info("SITE_URL environment variable not set")

    version = os.environ.get("MIKE_DOCS_VERSION")

    if version:
        log.info(f"Using MIKE_DOCS_VERSION environment variable: {version}")

    if not config["site_url"].endswith("/"):
        config["site_url"] += "/"

    log.info(f"site_url: {config['site_url']}")
    config["docs_version"] = version

    log.info(f"Set site_url to {config['site_url']}")
    os.environ["SITE_URL"] = config["site_url"]
    return config


def get_page_title(page_src: str, meta_data: dict) -> Optional[str]:
    """Returns the title of the page. The title in the meta data section
    will take precedence over the H1 markdown title if both are provided."""
    return (
        meta_data["title"]
        if "title" in meta_data and isinstance(meta_data["title"], str)
        else get_markdown_title(page_src)
    )
