import logging
import os
import re
from pathlib import Path
from urllib.parse import urljoin

from common.models import FileLoc, WikiLink
from fuzzywuzzy import fuzz  # type: ignore
from markdown.preprocessors import Preprocessor  # type: ignore
from mkdocs.structure.pages import Page

ROOT_DIR = Path(__file__).parent.parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"

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

log: logging.Logger = logging.getLogger("mkdocs")
SITE_URL = os.environ.get("SITE_URL", "/nspec/")
REPORT_BROKEN_WIKILINKS = bool(os.environ.get("REPORT_BROKEN_WIKILINKS", False))


class WLPreprocessor(Preprocessor):
    def __init__(self, mkconfig, snippet_preprocessor):
        self.mkconfig = mkconfig
        self.snippet_preprocessor = snippet_preprocessor
        self.current_file = None
        self.links_found = []

    def run(self, lines):
        lines = self.snippet_preprocessor.run(lines)
        config = self.mkconfig
        current_page_url = None

        in_code_block = False
        in_html_comment = False
        in_script = False

        inside_wikilink = False
        wikilink_buffer = []
        wikilink_buffer_pos = []

        if "current_page" in config and isinstance(config["current_page"], Page):
            page = config["current_page"]
            url_relative = DOCS_DIR / Path(page.url.replace(".html", ".md"))
            current_page_url = url_relative.as_posix()
            log.debug(f"CURRENT PAGE: {current_page_url}")

        if not current_page_url:
            log.error("Current page URL not found. Wikilinks will not be processed.")
            return lines

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

            # If we're inside a wikilink, keep adding lines to the buffer
            if inside_wikilink:
                wikilink_buffer.append(line)
                wikilink_buffer_pos.append(i)
                if "]]" in line:
                    # End of the wikilink
                    inside_wikilink = False
                    combined_wikilink = "".join(wikilink_buffer)
                    matches = WIKILINK_PATTERN.finditer(combined_wikilink)
                    self.generate_wikilink(
                        config,
                        wikilink_buffer_pos[0],
                        lines,
                        matches,
                        current_page_url,
                        wikilink_buffer[0],
                    )
                    # clean next lines
                    for pos in wikilink_buffer_pos[1:]:
                        lines[pos] = ""
                    wikilink_buffer = []
                    continue
            else:
                # Check if the line starts a new wikilink
                count_open, count_close = count_bracket_pairs(line)
                if "[[" in line and "]]" not in line:
                    inside_wikilink = True
                    wikilink_buffer_pos.append(i)
                    wikilink_buffer.append(line)
                if count_open != count_close and count_close > 0:
                    inside_wikilink = True
                    last_pos = line.rfind("[[")
                    last_partial = line[last_pos:]
                    wikilink_buffer.append(last_partial)
                    wikilink_buffer_pos.append(i)

            self.generate_wikilink(config, i, lines, matches, current_page_url)
        return lines

    def generate_wikilink(
        self, config, i, lines, matches, current_page_url, partial: str = ""
    ):
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
            if (
                len(config["url_for"].get(link_page, [])) > 1
                and link_page in config["url_for"]
            ):
                possible_pages = config["url_for"][link_page]

                # heuristic to suggest the most likely page
                hint = link.hint if link.hint else ""
                token = hint + link_page

                def fun_normalise(s):
                    return (
                        s.replace("_", " ")
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
                    f"""{loc}\nReference: '{link_page}' at '{loc}' is ambiguous. It could refer to any of the
                    following pages:\n  {_list}\nPlease revise the page alias or add a path hint to disambiguate,
                    e.g. [[folderHintA/subfolderHintB:page#anchor|display text]]. """
                )

                config["wikilinks_issues"] += 1
                config["url_for"][link_page] = [sorted_pages[0]]

            if (
                link_page in config["url_for"]
                and len(config["url_for"][link_page]) == 1
            ):
                if "url_for" not in config:
                    config["url_for"] = {}
                path = config["url_for"][link_page][0]
                page = match.group("page").strip()
                if page in config["url_for"]:
                    url_page = config["url_for"][page][0]
                    if url_page in config["nodes"]:
                        actuallink = config["nodes"][url_page]
                        if actuallink:
                            pageName = ""
                            if (
                                "names" in actuallink["page"]
                                and len(actuallink["page"]["names"]) > 0
                            ):
                                pageName = actuallink["page"]["names"][0]

                            self.links_found.append(
                                {
                                    "index": actuallink["index"],
                                    "path": actuallink["page"]["path"],
                                    "url": path.replace(".md", ".html"),
                                    "name": pageName,
                                }
                            )
                    else:
                        config["wikilinks_issues"] += 1
                else:
                    config["wikilinks_issues"] += 1

                html_path = urljoin(
                    config["site_url"],
                    path.replace(".juvix", "").replace(".md", ".html"),
                )

                md_link = f"[{link.display or link.page}]({html_path}{f'#{link.anchor}' if link.anchor else ''})"

                lines[i] = lines[i].replace(
                    partial if partial else match.group(0), md_link
                )

                log.debug(
                    f"{loc}:\nResolved link for page:\n  {link_page} -> {html_path}"
                )

            else:
                msg = f"{loc}:\nUnable to resolve reference\n  {link_page}"

                if REPORT_BROKEN_WIKILINKS:
                    log.warning(msg)

                lines[i] = lines[i].replace(match.group(0), link.text)
                config["wikilinks_issues"] += 1

        if len(self.links_found) > 0:
            config.update({"links_number": self.links_found})
        return lines


def count_bracket_pairs(text: str):
    # Count occurrences of [[ and ]]
    count_open = text.count("[[")
    count_close = text.count("]]")
    return count_open, count_close
