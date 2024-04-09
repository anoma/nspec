"""
Add better support for wiki-style links in MkDocs in tandem of pydownx_snippets,
that existing plugins out there.
"""

import re
import os
import mkdocs.plugins
import logging
from typing import List, Optional
from pymdownx.snippets import SnippetPreprocessor  # type: ignore
from pymdownx.snippets import DEFAULT_URL_SIZE, DEFAULT_URL_TIMEOUT  # type: ignore
from pathlib import Path
from mkdocs.utils import meta
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files
from mkdocs.config.defaults import MkDocsConfig
from markdown.preprocessors import Preprocessor  # type: ignore
from markdown.extensions import Extension  # type: ignore
from fuzzywuzzy import fuzz  # type: ignore
from common.models import WikiLink, FileLoc
from common.utils import fix_url, get_page_title

log: logging.Logger = logging.getLogger("mkdocs")

INDEXES_DIR = Path("docs/indexes")
INDEXES_DIR.mkdir(parents=True, exist_ok=True)

ROOT_DIR = Path(__file__).parent.parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"

SITE_URL = os.environ.get("SITE_URL", "/nspec/")
REPORT_BROKEN_WIKILINKS = bool(os.environ.get("REPORT_BROKEN_WIKILINKS", False))

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
    if "pymdownx.snippets" in config["markdown_extensions"]:
        config["markdown_extensions"].remove("pymdownx.snippets")
    wl_extension = WLExtension(mkconfig=config)
    config.markdown_extensions.append(wl_extension)  # type: ignore
    # exit()
    return config


def on_pre_build(config: MkDocsConfig) -> None:
    if not Path(INDEXES_DIR / "aliases.md").exists():
        with open(INDEXES_DIR / "aliases.md", "w") as f:
            f.write("# Links \n\n")

    config["to_url"] = {}
    config["from_url"] = {}

    config["aliases_for"] = {}
    config["url_for"] = {}

    config["wikilinks_issues"] = 0

    for url, page in _extract_aliases_from_nav(config["nav"]):
        config["aliases_for"][url] = [page]
        if not page in config["url_for"]:
            config["url_for"][page] = [url]
        else:
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

                        url = (Path(".") / Path(file.src_uri)).as_posix()

                        config["url_for"][_title] = [url]
                        config["aliases_for"][url] = [_title]
                    else:
                        log.debug(
                            f"Title '{_title}' is already in use, so it will not be added to the aliases table for '{url}'"
                        )

    with open(DOCS_DIR / "indexes" / "aliases.md", "w") as f:
        f.write(f"<h1>Aliases <small>({len(config['url_for'])})</small></h1>\n\n")
        current_letter = ""
        for_index = sorted(config["url_for"].keys()).copy()

        if "Aliases" in for_index:
            for_index.remove("Aliases")

        for alias in for_index:
            if alias[0].upper() != current_letter:
                current_letter = alias[0].upper()
                f.write(f"\n## {current_letter}\n\n")

            if len(config["url_for"][alias]) > 0:
                right_url = fix_url(
                    root=config["site_url"], url=config["url_for"][alias][0], html=True
                )
                f.write(f"- [{alias}]({right_url})\n")


def on_post_build(config: MkDocsConfig):
    log.info(f"Found {config['wikilinks_issues']} wikilinks issues.")

    """Executed after the build ends. Writes the aliases to a markdown file."""
    with open(INDEXES_DIR / "aliases.txt", "a") as f:
        f.write(f"\n\n## Aliases\n\n")
        for alias, urls in config["aliases_for"].items():
            f.write(f"- [{alias}]({urls[0]})\n")
            for url in urls[1:]:
                f.write(f"  - [{url}]({url})\n")


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
        _lines = self.snippet_preprocessor.run(lines)
        return self._run(_lines)

    def _run(self, lines):
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
                    fileloc=loc,
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

                    if len(list_possible_pages_with_score) > 1:
                        list_possible_pages_with_score[0] = (
                            f"{list_possible_pages_with_score[0]} (most likely, used for now)"
                        )
                    _list = "\n  ".join(list_possible_pages_with_score)

                    log.warning(
                        f"""{loc}\nReference: '{link_page}' at '{loc}' is ambiguous. It could refer to any of the following pages:\n  {_list}\nPlease revise the page alias or add a path hint to disambiguate, e.g. [[folderA/subfolderB:page#anchor|display text]]."""
                    )

                    config["wikilinks_issues"] += 1
                    config["url_for"][link_page] = [sorted_pages[0]]

                if (
                    link_page in config["url_for"]
                    and len(config["url_for"][link_page]) == 1
                ):

                    path = config["url_for"][link_page][0]

                    root_url = config["site_url"]

                    if "127.0.0.1" in root_url or "localhost" in root_url:
                        root_url = SITE_URL

                    md_path = fix_url(root=root_url, url=path, html=True)

                    md_link = f"[{link.display or link.page}]({md_path}{f'#{link.anchor}' if link.anchor else ''})"

                    lines[i] = lines[i].replace(match.group(0), md_link)

                    log.debug(
                        f"{loc}:\nResolved link for page:\n  {link_page} -> {md_path}"
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
    """Replace wikilinks by markdown links. This process avoids to replace links
    inside code blocks and html comments.
    """
    config["current_page"] = page  # needed for the preprocessor
    md_path = "./" + page.url.replace(".html", ".md")
    if md_path not in config["aliases_for"]:
        log.debug(f"""{md_path} is not linked in the navigation.""")
    return markdown


# AUXILIARY FUNCTIONS ----------------------------------------------


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
