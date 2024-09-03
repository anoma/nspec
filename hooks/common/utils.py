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


def generate_structure_graphviz(relations: List[ResultEntry]) -> str:
    """
    Generate a DOT structure for Graphviz from a list of objects with indexes and relations.

    Args:
        relations (list): A list of dictionaries, where each dictionary has 'index' and 'matches'.

    Returns:
        str: A DOT structure representing the graph.
    """
    dot_lines = ["digraph G {"]
    dot_lines_relations = [""]
    listed = []
    # Add nodes
    for relation in relations:
        index = relation.index
        file = relation.file
        url = relation.url
        if index not in listed:
            listed.append(int(index))
            dot_lines.append(f'  {index} [label="{file}" , href="{url}"];')
        for match in relation.matches:
            dot_lines_relations.append(f'  {index} -> {match["index"]} ;')
            if int(match["index"]) not in listed:
                listed.append(match["index"])
                dot_lines.append(
                    f'  {match["index"]} [label="{match["path"]}" , href="{match["url"]}"];'
                )

    dot_lines = [*dot_lines, *dot_lines_relations]
    dot_lines.append("}")
    return "\n".join(dot_lines)


def save_dot_and_generate(
    dot_structure: List[str],
    dot_file_path: str,
    format: str,
    file_path: str = None,
):
    """
    Save the DOT structure to a file and generate a PNG image using Graphviz.

    Args:
        dot_structure (str): The DOT structure as a string.
        dot_file_path (str): The path to save the DOT file.
        png_file_path (str): The path to save the PNG file.
    """
    # Save the DOT structure to a file
    with open(dot_file_path, "w") as file:
        file.write(dot_structure)

    if not GRAPHVIZ_AVAILABLE:
        log.error("Graphviz not available. Skipping PNG generation.")
        return

    # Generate PNG image using graphviz
    graph = graphviz.Source(dot_structure)
    graph.render(dot_file_path, format=format)

    file_path = file_path + "." + format
    # Rename the generated file to the desired PNG file path
    if file_path:
        # Handle existing file by removing it first

        if Path(file_path).exists():
            try:
                os.remove(file_path)
            except Exception as e:
                log.error(f"Error removing {file_path}: {e}")

        os.rename(f"{dot_file_path}." + format, file_path)


def generate_structure_mermaid(relations: List[ResultEntry]) -> str:
    """
    Generate a Mermaid diagram structure from a list of objects with indexes and relations.

    Args:
        relations (list): A list of dictionaries, where each dictionary has 'index' and 'matches'.

    Returns:
        str: A Mermaid diagram structure representing the graph.
    """
    mermaid_lines = []
    mermaid_lines_relation = ["graph TD"]
    listed = []

    # Add nodes and edges
    for relation in relations:
        index = relation.index
        file = relation.file
        url = relation.url
        if index not in listed:
            listed.append(int(index))
            mermaid_lines.append(f' click {index} "{url}" _blank')
        for match in relation.matches:
            if int(match["index"]) not in listed:
                listed.append(match["index"])
                mermaid_lines.append(f' click {match["index"]} "{match["url"]}" _blank')
            mermaid_lines_relation.append(
                f'  {index}["{file}"] --> {match["index"]}["{match["path"]}"]'
            )

    mermaid_lines = [*mermaid_lines_relation, *mermaid_lines]
    return "\n".join(mermaid_lines)
