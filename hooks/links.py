"""
Add better support for wiki-style links in MkDocs in tandem of pydownx_snippets,
that existing plugins out there.
"""

import json
import logging
import os
import re
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin

import mkdocs.plugins
from common.models import FileLoc, WikiLink
from common.utils import fix_site_url, get_page_title
from fuzzywuzzy import fuzz  # type: ignore
from markdown.extensions import Extension  # type: ignore
from markdown.preprocessors import Preprocessor  # type: ignore
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.utils import meta
from pymdownx.snippets import DEFAULT_URL_SIZE, DEFAULT_URL_TIMEOUT, SnippetPreprocessor

log: logging.Logger = logging.getLogger("mkdocs")

ROOT_DIR = Path(__file__).parent.parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"

SITE_URL = os.environ.get("SITE_URL", "/nspec/")
REPORT_BROKEN_WIKILINKS = bool(os.environ.get("REPORT_BROKEN_WIKILINKS", False))

CACHE_DIR: Path = ROOT_DIR.joinpath(".hooks")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

LINKS_JSON = CACHE_DIR / "aliases.json"

""" Example of a wikilink with a path hint:
[[path-hint:page#anchor|display text]]
"""

WIKILINK_PATTERN = re.compile(
    r"""
(?:\\)?\[\[
(?:(?P<hint>[^:|\]]+):)?
(?P<page>[^|\]#]+)
(?:\#(?P<anchor>[^|\]]+))?
(?:\|(?P<display>[^\]]+))?
\]\]
""",
    re.VERBOSE,
)


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

    for _url, page in _extract_aliases_from_nav(config["nav"]):
        url = urljoin(config["site_url"], _url)
        config["aliases_for"][url] = [page]
        config["url_for"].setdefault(page, [])
        config["url_for"][page].append(url)

    config["current_page"] = None  # current page being processed


def on_files(files: Files, config: MkDocsConfig) -> None:
    """When MkDocs loads its files, extract aliases from any Markdown files
    that were found.
    """
    for file in filter(lambda f: f.is_documentation_page(), files):
        with open(file.abs_src_path, encoding="utf-8-sig", errors="strict") as handle:
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
        sc = self.mkconfig.mdx_configs["pymdownx.snippets"]
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


class WLPreprocessor(Preprocessor):
    def __init__(self, mkconfig, snippet_preprocessor):
        self.mkconfig = mkconfig
        self.snippet_preprocessor = snippet_preprocessor

    def run(self, lines):
        lines = self.snippet_preprocessor.run(lines)
        config = self.mkconfig
        current_page_url = None

        if "current_page" in config and isinstance(config["current_page"], Page):

            url_relative = DOCS_DIR / Path(
                config["current_page"].url.replace(".html", ".md")
            )
            current_page_url = url_relative.as_posix()

            log.debug(f"CURRENT PAGE: {current_page_url}")

        if not current_page_url:
            log.error("Current page URL not found. Wikilinks will not be processed.")
            return lines

        in_code_block = False
        in_html_comment = False
        in_script = False

        for i, line in enumerate(lines.copy()):
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
            if "<!--" in line:
                in_html_comment = True
            if "-->" in line:
                in_html_comment = False
            if "<script" in line:
                in_script = True
            if "</script>" in line:
                in_script = False
            if in_code_block or in_html_comment or in_script:
                continue

            matches = WIKILINK_PATTERN.finditer(line)

            for match in matches:

                loc = FileLoc(current_page_url, i + 1, match.start() + 2)

                link = WikiLink(
                    page=match.group("page"),
                    hint=match.group("hint"),
                    anchor=match.group("anchor"),
                    display=match.group("display"),
                    loc=loc,
                )

                link_page = link.page.replace("-", " ")

                if len(config["url_for"].get(link_page, [])) > 1:

                    possible_pages = config["url_for"][link_page]

                    # heuristic to suggest the most likely page
                    hint = link.hint if link.hint else ""
                    token = hint + link_page
                    fun_normalise = (
                        lambda s: s.replace("_", " ")
                        .replace("-", " ")
                        .replace(":", " ")
                        .replace("/", " ")
                        .replace(".md", "")
                    )
                    coefficients = {
                        p: fuzz.WRatio(fun_normalise(p), token) for p in possible_pages
                    }
                    sorted_pages = sorted(
                        possible_pages, key=lambda p: coefficients[p], reverse=True
                    )

                    list_possible_pages_with_score = [
                        f"{p} ({coefficients[p]})" for p in sorted_pages
                    ]

                    list_possible_pages_with_score[0] = (
                        f"{list_possible_pages_with_score[0]} (most likely, used for now)"
                    )

                    _list = "\n  ".join(list_possible_pages_with_score)

                    log.warning(
                        f"""{loc}\nReference: '{link_page}' at '{loc}' is ambiguous. It could refer to any of the following pages:\n  {_list}\nPlease revise the page alias or add a path hint to disambiguate, e.g. [[folderHintA/subfolderHintB:page#anchor|display text]]."""
                    )

                    config["wikilinks_issues"] += 1
                    config["url_for"][link_page] = [sorted_pages[0]]

                if (
                    link_page in config["url_for"]
                    and len(config["url_for"][link_page]) == 1
                ):

                    path = config["url_for"][link_page][0]

                    html_path = urljoin(
                        config["site_url"],
                        path.replace(".juvix", "").replace(".md", ".html"),
                    )

                    md_link = f"[{link.display or link.page}]({html_path}{f'#{link.anchor}' if link.anchor else ''})"

                    lines[i] = lines[i].replace(match.group(0), md_link)

                    log.debug(
                        f"{loc}:\nResolved link for page:\n  {link_page} -> {html_path}"
                    )
                else:
                    msg = f"{loc}:\nUnable to resolve reference\n  {link_page}"

                    if REPORT_BROKEN_WIKILINKS:
                        log.warning(msg)

                    lines[i] = lines[i].replace(match.group(0), link.text)
                    config["wikilinks_issues"] += 1
        return lines


@mkdocs.plugins.event_priority(-200)
def on_page_markdown(markdown, page: Page, config: MkDocsConfig, files: Files) -> str:
    config["current_page"] = page  # needed for the preprocessor
    return markdown


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
