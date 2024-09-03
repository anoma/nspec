"""
Support for wiki-style links in MkDocs in tandem of pydownx_snippets.
"""

import json
import logging
import os
import re
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin

import mkdocs.plugins
from common.models.entry import ResultEntry
from common.preprocesors.links import WLPreprocessor
from common.utils import fix_site_url, generate_structure_mermaid, get_page_title
from markdown.extensions import Extension  # type: ignore
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.utils import meta
from snippets import DEFAULT_URL_SIZE, DEFAULT_URL_TIMEOUT, SnippetPreprocessor

log: logging.Logger = logging.getLogger("mkdocs")

ROOT_DIR = Path(__file__).parent.parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"

SITE_URL = os.environ.get("SITE_URL", "/nspec/")
REPORT_BROKEN_WIKILINKS = bool(os.environ.get("REPORT_BROKEN_WIKILINKS", False))

CACHE_DIR: Path = ROOT_DIR.joinpath(".hooks")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

LINKS_JSON = CACHE_DIR / "aliases.json"
GRAPH_JSON = CACHE_DIR / "graph.json"
NODES_JSON = CACHE_DIR / "nodes.json"
SITE_MAPS_GRAPH = CACHE_DIR / "site_maps_graph"
SITE_MAPS_GRAPH.mkdir(parents=True, exist_ok=True)


files_relation: List[ResultEntry] = []


class WLExtension(Extension):

    def __init__(self, mkconfig):
        self.mkconfig = mkconfig

        if "pymdownx.snippets" in self.mkconfig.mdx_configs:
            bpath = self.mkconfig.mdx_configs["pymdownx.snippets"].get(
                "base_path", [".", "includes"]
            )

            excluded_dirs = [".", "__", "site", "env", "venv"]

            for root, dirs, _ in os.walk("."):
                dirs[:] = [
                    d
                    for d in dirs
                    if not any(d.startswith(exclude) for exclude in excluded_dirs)
                ]

                bpath.extend(os.path.relpath(os.path.join(root, d), ".") for d in dirs)

            self.mkconfig.mdx_configs["pymdownx.snippets"]["base_path"] = bpath

    def __repr__(self):
        return "WLExtension"

    def extendMarkdown(self, md):  # noqa: N802

        self.md = md
        md.registerExtension(self)

        # Snippet extension preprocessor
        sc = self.mkconfig.mdx_configs.get("pymdownx.snippets", {})
        sc.setdefault("dedent_subsections", True)
        sc.setdefault("url_request_headers", {})
        sc.setdefault("url_timeout", DEFAULT_URL_TIMEOUT)
        sc.setdefault("url_max_size", DEFAULT_URL_SIZE)
        sc.setdefault("url_download", True)
        sc.setdefault("auto_append", [])
        sc.setdefault("check_paths", True)
        sc.setdefault("encoding", "utf-8")
        sc.setdefault("restrict_base_path", True)
        sc.setdefault("base_path", [".", "includes"])

        sp = SnippetPreprocessor(sc, md)
        self.wlpp = WLPreprocessor(self.mkconfig, sp)
        md.preprocessors.register(self.wlpp, "wl-pp", 100)


def on_config(config: MkDocsConfig, **kwargs) -> MkDocsConfig:
    config = fix_site_url(config)
    if "pymdownx.snippets" in config["markdown_extensions"]:
        config["markdown_extensions"].remove("pymdownx.snippets")
    wl_extension = WLExtension(mkconfig=config)
    config.markdown_extensions.append(wl_extension)  # type: ignore
    return config


def on_pre_build(config: MkDocsConfig) -> None:
    config["aliases_for"] = {}
    config["url_for"] = {}
    config["wikilinks_issues"] = 0
    config["nodes"] = {}
    config["reations"] = []
    node_index = 0

    for _url, page in _extract_aliases_from_nav(config["nav"]):
        url = urljoin(config["site_url"], _url)

        config["aliases_for"][url] = [page]
        config["url_for"].setdefault(page, [])
        config["url_for"][page].append(url)

        # Create a new entry if the URL is not already present in config["nodes"]
        if url not in config["nodes"]:
            config["nodes"][url] = {
                "index": node_index,
                "page": {"names": [], "path": _url.replace("./", "")},
            }
        # Append the page to the "names" list
        config["nodes"][url]["page"]["names"].append(page)
        node_index += 1

    if NODES_JSON.exists():
        NODES_JSON.unlink()

    with open(NODES_JSON, "w") as f:
        json.dump(
            {
                "nodes": config.get("nodes", {}),
            },
            f,
            indent=2,
        )
    config["current_page"] = None  # current page being processed


def on_files(files: Files, config: MkDocsConfig) -> None:
    """When MkDocs loads its files, extract aliases from any Markdown files
    that were found.
    """
    for file in filter(lambda f: f.is_documentation_page(), files):
        pathFile: str | None = file.abs_src_path
        if pathFile is not None:
            with open(pathFile, encoding="utf-8-sig", errors="strict") as handle:
                source, meta_data = meta.get_data(handle.read())
                alias_names: Optional[List[str]] = _get_alias_names(meta_data)

                if alias_names is None or len(alias_names) < 1:
                    _title: Optional[str] = get_page_title(source, meta_data)

                    if _title:
                        _title = _title.strip()
                        _title = re.sub(r'^[\'"`]|["\'`]$', "", _title)

                        if _title not in config["url_for"]:
                            url = urljoin(config["site_url"], file.url)
                            config["url_for"][_title] = [url]
                            config["aliases_for"][url] = [_title]

    if LINKS_JSON.exists():
        LINKS_JSON.unlink()

    with open(LINKS_JSON, "w") as f:
        json.dump(
            {
                "aliases_for": config.get("aliases_for", {}),
                "url_for": {
                    k: [
                        p.replace(".md", ".html") if p.endswith(".md") else p for p in v
                    ]
                    for k, v in config["url_for"].items()
                },
            },
            f,
            indent=2,
        )


@mkdocs.plugins.event_priority(-200)
def on_page_markdown(markdown, page: Page, config: MkDocsConfig, files: Files) -> str:
    config["current_page"] = page  # needed for the preprocessor
    return markdown


def on_page_content(html, page: Page, config: MkDocsConfig, files: Files) -> str:
    if "current_page" not in config or "nodes" not in config:
        return html
    current_page = config["current_page"]
    url = current_page.canonical_url.replace(".html", ".md")
    if url not in config["nodes"]:
        return html

    # at this point, the preprocessor has already run
    # so we can safely access the linksNumber
    links_number = config.get("links_number", {})
    if url not in config["links_number"] or "index" not in config["nodes"][url]:
        return html

    if links_number:

        actualindex = config["nodes"][url]["index"]
        result_entry = ResultEntry(
            file=current_page.url,
            index=actualindex,
            matches=links_number,
            url=current_page.canonical_url,
        )
        files_relation.append(result_entry)
        mermaid_structure = generate_structure_mermaid([result_entry])
        file_path = result_entry.file.replace("\\", "_").replace("/", "_")
        file_path = (SITE_MAPS_GRAPH / file_path).as_posix()

        wrapped_mermaid = (
            '\n<details class="note" open="">\n'
            "    <summary>Link Graph</summary>\n"
            '    <figure markdown="span">\n'
            "        <p></p>\n"
            f'        <div class="mermaid">\n{mermaid_structure}\n</div>\n'
            '        <figcaption markdown="span">Link Diagram</figcaption>\n'
            "    </figure>\n"
            "    <p></p>\n"
            "</details>\n"
        )
        html += wrapped_mermaid
    return html


def _extract_aliases_from_nav(item, parent_key=None):
    result = []
    if isinstance(item, str):
        if parent_key:
            result.append((item, parent_key))
    elif isinstance(item, list):
        for i in item:
            result.extend(_extract_aliases_from_nav(i, parent_key))
    elif isinstance(item, dict):
        for k, v in item.items():
            if isinstance(v, str):
                result.append((v, k))
            else:
                result.extend(_extract_aliases_from_nav(v, k))
    return result


def _get_alias_names(meta_data: dict):
    """Returns the list of configured alias names."""
    if len(meta_data) <= 0 or "alias" not in meta_data:
        return None
    aliases = meta_data["alias"]
    if isinstance(aliases, list):
        return list(filter(lambda value: isinstance(value, str), aliases))
    if isinstance(aliases, dict) and "name" in aliases:
        return [aliases["name"]]
    if isinstance(aliases, str):
        return [aliases]
    return None
