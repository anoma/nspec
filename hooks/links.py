
"""
Add support for wiki-style links in MkDocs in tandem for snippets. Generate a
graph of references between pages. Self-contained plugin that does not require
any external dependencies, as it's being used as a hook in the MkDocs build
process.
"""

import re
import os
import mkdocs.plugins
import logging
from typing import Any, Callable, List, Optional, Tuple, Dict, Set
from pymdownx.snippets import SnippetExtension, SnippetPreprocessor  # type: ignore
from pymdownx.snippets import DEFAULT_URL_SIZE,  DEFAULT_URL_TIMEOUT  # type: ignore
from pathlib import Path
from mkdocs.utils import meta, get_markdown_title, get_relative_url
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File, Files
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.config import Config, config_options
from markdown.preprocessors import Preprocessor  # type: ignore
from markdown.extensions import Extension  # type: ignore
from fuzzywuzzy import fuzz  # type: ignore

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


def on_config(config: MkDocsConfig, **kwargs):
    if 'pymdownx.snippets' in config['markdown_extensions']:
        config['markdown_extensions'].remove('pymdownx.snippets')
    config.markdown_extensions.append(WLExtension(config))
    return config


def on_pre_build(config: MkDocsConfig):
    if not Path(INDEXES_DIR / 'aliases.md').exists():
        with open(INDEXES_DIR / 'aliases.md', 'w') as f:
            f.write("# Aliases\n\n")

    config['to_url'] = {}
    config['from_url'] = {}

    config['aliases_for'] = {}
    config['url_for'] = {}

    config['wikilinks_issues'] = 0

    for url, page in _extract_aliases_from_nav(config['nav']):
        config['aliases_for'][url] = [page]
        if not page in config['url_for']:
            config['url_for'][page] = [url]
        else:
            config['url_for'][page].append(url)
    config['current_page'] = None  # current page being processed


class WLExtension(Extension):

    def __init__(self, mkconfig):
        self.mkconfig = mkconfig

        if 'pymdownx.snippets' in self.mkconfig.mdx_configs:
            bpath = self.mkconfig.mdx_configs['pymdownx.snippets']\
                .get('base_path', ['.', 'includes'])

            excluded_dirs = ['.', '__', 'site', 'env', 'venv']

            for root, dirs, _ in os.walk('.'):
                dirs[:] = [d for d in dirs if not
                           any(d.startswith(exclude) for exclude in excluded_dirs)]

                bpath.extend(os.path.relpath(
                    os.path.join(root, d), '.') for d in dirs)

            self.mkconfig.mdx_configs['pymdownx.snippets']['base_path'] = bpath

    def extendMarkdown(self, md):  # noqa: N802

        self.md = md
        md.registerExtension(self)

        # Snippet extension preprocessor
        sc = self.mkconfig.mdx_configs['pymdownx.snippets']
        sc.setdefault('dedent_subsections', True)
        sc.setdefault('url_request_headers', {})
        sc.setdefault('url_timeout', DEFAULT_URL_TIMEOUT)
        sc.setdefault('url_max_size', DEFAULT_URL_SIZE)
        sc.setdefault('url_download', True)
        sc.setdefault('auto_append', [])
        sc.setdefault('check_paths', True)
        sc.setdefault('encoding', 'utf-8')
        sc.setdefault('restrict_base_path', True)
        sc.setdefault('base_path', ['.', 'includes'])

        sp = SnippetPreprocessor(sc, md)
        self.wlpp = WLPreprocessor(self.mkconfig, sp)
        md.preprocessors.register(self.wlpp, 'wl-pp', 50)


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
        if 'current_page' in config and isinstance(config['current_page'], Page):
            url_relative = DOCS_DIR / \
                Path(config['current_page'].url.replace('.html', '.md'))
            current_page_url = url_relative.as_posix()
        
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
                ocurrence = Ocurrence(current_page_url,
                                      i + 1, match.start() + 2)

                if not link.page in config['url_for']:
                    
                    log.debug(f"{ocurrence}\n'{link.text}'does target a non-existing page. Check the aliases in the navigation or on each page.")
                    
                    lines[i] = lines[i].replace(match.group(0),
                                                link.text)
                    
                    config['wikilinks_issues'] += 1

                elif len(config['url_for'][link.page]) > 1:

                    possible_pages = "\n- ".join(config['url_for'][link.page])

                    log.warning(f"""{ocurrence}\nReference: {link.text} at '{ocurrence}' is ambiguous. It could refer to any of the following pages:\n{possible_pages}\n
                    Please revise the page alias or add a path hint to disambiguate, e.g. [[folderA/subfolderB:page#anchor|display text]].""")

                    config['wikilinks_issues'] += 1

                elif len(config['url_for'][link.page]) == 1:
                    path = config['url_for'][link.page][0]
                    md_link = link.to_markdown(path)
                    lines[i] = lines[i].replace(match.group(0), md_link)
        return lines


@mkdocs.plugins.event_priority(-200)
def on_page_markdown(markdown, page: Page, config: MkDocsConfig, files: Files) -> str:
    """Replace wikilinks by markdown links. This process avoids to replace links
#     inside code blocks and html comments.
#     """
    config['current_page'] = page # needed for the preprocessor
    md_path = "./" + page.url.replace(".html", ".md")
    if md_path not in config['aliases_for']:
        # The page could be a draft or a work in progress. Or simply,
        # the page is not linked in the navigation, on purpose.
        log.debug(f"""{md_path} is not linked in the navigation.""")
    return markdown
#     if "ordering-v1" in md_path:
#         print(markdown)
#         exit()

#     lines = markdown.split('\n')

#     in_code_block = False
#     in_html_comment = False
#     in_script = False
#     in_div = False

#     for i, line in enumerate(lines.copy()):
#         if line.strip().startswith('```'):
#             in_code_block = not in_code_block
#         if '<!--' in line:
#             in_html_comment = True
#         if '-->' in line:
#             in_html_comment = False
#         if '<script' in line:
#             in_script = True
#         if '</script>' in line:
#             in_script = False
#         if '<div' in line:
#             in_div = True
#         if '</div>' in line:
#             in_div = False
#         if in_code_block or in_html_comment or in_script or in_div:
#             continue
#         matches = WIKILINK_PATTERN.finditer(line)

#         for match in matches:
#             link = WikiLink(page=match.group('page'), hint=match.group('hint'), anchor=match.group('anchor'),
#                             display=match.group('display'))
#             ocurrence = Ocurrence(url_relative.as_posix(),
#                                   i + 1, match.start() + 2)

#             if not link.page in config['url_for']:
#                 # log.info(f"{ocurrence}\n'{link.text}'does target a non-existing page.")
#                 lines[i] = lines[i].replace(match.group(0),
#                                             link.text)
#                 config['wikilinks_issues'] += 1

#             elif len(config['url_for'][link.page]) > 1:

#                 possible_pages = "\n- ".join(config['url_for'][link.page])

#                 log.warning(f"""{link.text} at '{ocurrence}' is ambiguous. It could refer to any of the following pages:\n{possible_pages}\n
#                 Please add a path hint to disambiguate, e.g. [[folderA/subfolderB:page#anchor|display text]].""")
#                 config['wikilinks_issues'] += 1

#             elif len(config['url_for'][link.page]) == 1:
#                 path = config['url_for'][link.page][0]
#                 md_link = link.to_markdown(path)
#                 lines[i] = lines[i].replace(match.group(0), md_link)
#     return '\n'.join(lines)

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
