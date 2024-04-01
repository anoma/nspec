
"""
Add support for wiki-style links in MkDocs in tandem for snippets. Generate a
graph of references between pages. Self-contained plugin that does not require
any external dependencies, as it's being used as a hook in the MkDocs build
process.
"""

from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page
from mkdocs.utils import meta, get_markdown_title, get_relative_url
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple, Dict, Set
import logging
import re
import os
from fuzzywuzzy import fuzz  # type: ignore

import mkdocs.plugins

from mkdocs.config import Config


from markdown.extensions import Extension  # type: ignore
from markdown.preprocessors import Preprocessor  # type: ignore
from pymdownx.snippets import SnippetExtension, SnippetPreprocessor  # type: ignore

log: logging.Logger = logging.getLogger('mkdocs')

INDEXES_DIR = Path('docs/indexes')
INDEXES_DIR.mkdir(parents=True, exist_ok=True)

ROOT_DIR = Path(__file__).parent.parent.absolute()
DOCS_DIR = ROOT_DIR / 'docs'

""" Example of a wikilink with a path hint:
[[path-hint:page#anchor|display text]]
"""

WIKILINK_PATTERN = re.compile(r"""
(?:\\)?\[\[
(?:(?P<hint>[^:]+):)?
(?P<page>[^|\]#]+)
(?:\#(?P<anchor>[^|\]]+))?
(?:\|(?P<display>[^\]]+))?
\]\]
""", re.VERBOSE)

class Ocurrence:
    path: str
    line: int
    column: int = 0

    def __init__(self, path: str, line: int, column: int):
        self.path = path
        self.line = line
        self.column = column

    def __str__(self):
        return f"{self.path}:{self.line}:{self.column}"


class WikiLink:
    def __init__(self, page: str, hint: Optional[str] = None, anchor: Optional[str] = None, display: Optional[str] = None):
        self.page: str = page.strip()
        self.hint: Optional[str] = hint.strip() if hint else None
        self.anchor: Optional[str] = anchor.strip() if anchor else None
        self.display: Optional[str] = display.strip() if display else None

    def __hash__(self):
        return hash(self.page)

    @property
    def text(self):
        if self.display:
            return self.display
        return self.page

    def __repr__(self):
        s = f"page={self.page}, "
        if self.hint:
            s += f"hint={self.hint}, "
        if self.anchor:
            s += f"anchor={self.anchor}, "
        if self.display:
            s += f"display={self.display}"
        return f"WikiLink({s})"

    def to_markdown(self, path):
        md_path = path.replace('./', '/nspec/').replace('.md', '.html')
        return f"[{self.display or self.page}]({md_path}{f'#{self.anchor}' if self.anchor else ''})"

def on_config(config, **kwargs):
    print(config)
    return config


# ------------------------------------------------------------------------------
# The generation of cross-references graph is currently limited to the
# navigation structure of the site. This limitation exists because this routine
# is executed before the actual build starts. Additional content is added to
# each markdown file at the end, in case it is referenced by a wikilink.


def on_pre_build(config: MkDocsConfig):
    """Executed before the build begins. Initializes the aliases dictionary
    and the alias issue and alias use counters.
    """
    if not Path(INDEXES_DIR / 'aliases.md').exists():
        with open(INDEXES_DIR / 'aliases.md', 'w') as f:
            f.write("# Aliases\n\n")

    # a graph where the nodes are the pages (src_path) and the edges are
    # determined by the (wikilinks) references, initially.

    # page --points to -> list[links]
    # link gives a age --is referenced by -> the current page

    config['to_url'] = {}
    config['from_url'] = {}

    config['url_alias'] = {}
    config['alias_url'] = {}

    config['wikilinks_issues'] = 0

    for url, page_alias in _extract_aliases_from_nav(config['nav']):
        config['url_alias'][url] = [page_alias]
        if not page_alias in config['alias_url']:
            config['alias_url'][page_alias] = [url]
        else:
            config['alias_url'][page_alias].append(url)

@mkdocs.plugins.event_priority(-200)
def on_page_markdown(markdown, page: Page, config: MkDocsConfig, files : Files) -> str:
    
    """Replace wikilinks by markdown links. This process avoids to replace links
    inside code blocks and html comments.
    """
    current_page = page
    md_path = "./" + current_page.url.replace(".html", ".md")

    if md_path not in config['url_alias']:
        # The page could be a draft or a work in progress. Or simply,
        # the page is not linked in the navigation, on purpose.
        log.debug(f"""{md_path} is not linked in the navigation.""")

    url_relative = DOCS_DIR / Path(current_page.url.replace('.html', '.md'))
    if "ordering-v1" in md_path:
        print(markdown)
        exit()


    lines = markdown.split('\n')

    in_code_block = False
    in_html_comment = False
    in_script = False
    in_div = False

    for i, line in enumerate(lines.copy()):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
        if '<!--' in line:
            in_html_comment = True
        if '-->' in line:
            in_html_comment = False
        if '<script' in line:
            in_script = True
        if '</script>' in line:
            in_script = False
        if '<div' in line:
            in_div = True
        if '</div>' in line:
            in_div = False
        if in_code_block or in_html_comment or in_script or in_div:
            continue
        matches = WIKILINK_PATTERN.finditer(line)

        for match in matches:
            link = WikiLink(page=match.group('page'), hint=match.group('hint'), anchor=match.group('anchor'),
                            display=match.group('display'))
            ocurrence = Ocurrence(url_relative.as_posix(),
                                  i + 1, match.start() + 2)

            if not link.page in config['alias_url']:
                # log.info(f"{ocurrence}\n'{link.text}'does target a non-existing page.")
                lines[i] = lines[i].replace(match.group(0),
                                            link.text)
                config['wikilinks_issues'] += 1

            elif len(config['alias_url'][link.page]) > 1:

                possible_pages = "\n- ".join(config['alias_url'][link.page])

                log.warning(f"""{link.text} at '{ocurrence}' is ambiguous. It could refer to any of the following pages:\n{possible_pages}\n
                Please add a path hint to disambiguate, e.g. [[folderA/subfolderB:page#anchor|display text]].""")
                config['wikilinks_issues'] += 1

            elif len(config['alias_url'][link.page]) == 1:
                path = config['alias_url'][link.page][0]
                md_link = link.to_markdown(path)
                lines[i] = lines[i].replace(match.group(0), md_link)
    return '\n'.join(lines)

# ------------------------------------------------------------------------------
# Helper functions

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


def _get_page_title(page_src: str, meta_data: dict) -> Optional[str]:
    """Returns the title of the page. The title in the meta data section
    will take precedence over the H1 markdown title if both are provided."""
    return (
        meta_data['title']
        if 'title' in meta_data and isinstance(meta_data['title'], str)
        else get_markdown_title(page_src)
    )


def _get_alias_names(meta_data: dict):
    """Returns the list of configured alias names."""
    if len(meta_data) <= 0 or 'alias' not in meta_data:
        return None
    aliases = meta_data['alias']
    if isinstance(aliases, list):
        # If the alias meta data is a list, ensure that they're strings
        return list(filter(lambda value: isinstance(value, str), aliases))
    if isinstance(aliases, dict) and 'name' in aliases:
        return [aliases['name']]
    if isinstance(aliases, str):
        return [aliases]
    return None
