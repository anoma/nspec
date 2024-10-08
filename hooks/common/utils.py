import logging
import os
from pathlib import Path
from typing import List, Optional

import graphviz
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.utils import get_markdown_title

from .models.entry import ResultEntry

log = logging.getLogger("mkdocs")
GRAPHVIZ_AVAILABLE = os.environ.get("GRAPHVIZ_AVAILABLE", True)


def fix_site_url(config: MkDocsConfig) -> MkDocsConfig:
    if os.environ.get("SITE_URL"):
        config["site_url"] = os.environ["SITE_URL"]
        if not config["site_url"].endswith("/"):
            config["site_url"] += "/"
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


def create_mermaid_diagram(relation_entries: List[ResultEntry]) -> str:
    mermaid_lines = []
    mermaid_lines_relation = ["graph TD"]
    listed = []

    # Add nodes and edges
    for relation in relation_entries:
        index = relation.index
        url = relation.url
        if index not in listed:
            listed.append(int(index))
            mermaid_lines.append(f' click {index} "{url}" _blank')
        for match in relation.matches:
            if int(match["index"]) not in listed:
                listed.append(match["index"])
                mermaid_lines.append(f' click {match["index"]} "{match["url"]}" _blank')
            mermaid_lines_relation.append(
                f'  {index}["{relation.name}"] --> {match["index"]}["{match["name"]}"]'
            )

    mermaid_lines = [*mermaid_lines_relation, *mermaid_lines]
    return "\n".join(mermaid_lines)
