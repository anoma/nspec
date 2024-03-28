
"""
Add support for wiki-style links in MkDocs. Generate a graph of references
between pages. Self-contained plugin that does not require any external
dependencies, as it's being used as a hook in the MkDocs build process.
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
from fuzzywuzzy import fuzz  # type: ignore

log: logging.Logger = logging.getLogger('mkdocs')

INDEXES_DIR = Path('docs/indexes')
INDEXES_DIR.mkdir(parents=True, exist_ok=True)

ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / 'docs'

""" Example of a wikilink:
[[path-hint:page#anchor|display text]]
"""
# Updated Regex Pattern to Include Optional Hint
WIKILINK_PATTERN = re.compile(r"""
(?:\\)?\[\[                      # Matches the start of a wikilink (optionally escaped)
(?:(?P<hint>[^:]+):)?            # Optionally captures the hint text before a colon
(?P<page>[^|\]#]+)               # Captures the page name (up to a |, ], or #)
(?:\#(?P<anchor>[^|\]]+))?       # Optionally captures the anchor (up to a | or ])
(?:\|(?P<display>[^\]]+))?       # Optionally captures the display text (up to a ])
\]\]                             # Matches the end of a wikilink
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
        self.references: List[Ocurrence] = []

    def __hash__(self):
        return hash(self.page)

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
        md_path =path.replace('./', '/nspec/').replace('.md', '.html')
        return f"[{self.display or self.page}]({md_path}{f'#{self.anchor}' if self.anchor else ''})"

    def add_reference(self, ocurrence: Ocurrence):
        self.references.append(ocurrence)

# ------------------------------------------------------------------------------
# The generation of cross-references graph is currently limited to the
# navigation structure of the site. This limitation exists because this routine
# is executed before the actual build starts. Additional content is added to
# each markdown file at the end, in case it is referenced by a wikilink.


def on_pre_build(config: MkDocsConfig):
    """Executed before the build begins. Initializes the aliases dictionary
    and the alias issue and alias use counters.
    """
    with open(INDEXES_DIR / 'aliases.md', 'w') as f:
        f.write("# Aliases\n\n")

    # a graph where the nodes are the pages (src_path) and the edges are
    # determined by the (wikilinks) references, initially.

    config['wikilinks'] = set()
    config['wikilinks_per_url'] = {}
    config['url_alias'] = {}
    config['alias_url'] = {}

    for url, page_alias in _extract_aliases_from_nav(config['nav']):
        config['url_alias'][url] = [page_alias]
        if not page_alias in config['alias_url']:
            config['alias_url'][page_alias] = [url]
        else:
            config['alias_url'][page_alias].append(url)

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

def on_post_build(config: MkDocsConfig):
    """Executed after the build ends. Writes the aliases to a markdown file."""
    with open(INDEXES_DIR / 'aliases.txt', 'a') as f:
        f.write(f"\n\n## Aliases\n\n")
        for alias, urls in config['alias_url'].items():
            f.write(f"- [{alias}]({urls[0]})\n")
            for url in urls[1:]:
                f.write(f"  - [{url}]({url})\n")

    with open(INDEXES_DIR / 'wikilinks.txt', 'w') as f:
        f.write(f"# Wikilinks\n\n")
        for url, wikilinks in config['wikilinks_per_url'].items():
            f.write(f"## {url}\n\n")
            for wikilink in wikilinks:
                f.write(f"- {wikilink}\n")
                for reference in wikilink.references:
                    f.write(f"  - {reference}\n")

    with open(INDEXES_DIR / 'wikilinks.dot', 'w') as f:
        f.write(f"digraph G {{\n")
        for wikilink in config['wikilinks']:
            for reference in wikilink.references:
                f.write(f'"{wikilink.page}" -> "{reference}"\n')
        f.write(f"}}\n")

def on_page_markdown(markdown: str, *, page: Page, config: MkDocsConfig, **_) -> str:
    """Replace wikilinks by markdown links. The preprocessing step
    should be smart, avoiding to replace links inside code blocks, html
    comments, and mermaid diagrams.
    """

    current_page = page
    url_relative = DOCS_DIR / Path(current_page.url.replace('.html', '.md'))

    lines = markdown.split('\n')
    for i, line in enumerate(lines.copy()):
        matches = WIKILINK_PATTERN.finditer(line)
        for match in matches:
            link = WikiLink(page=match.group('page'), hint=match.group('hint'), anchor=match.group('anchor'),
                            display=match.group('display'))
            ocurrence = Ocurrence(url_relative.as_posix(), i + 1, match.start())
            link.add_reference(ocurrence)
            if not link.page in config['alias_url']:
                log.warning(f"{link} at '{ocurrence}' is not defined in the navigation.")
            else:
                if len(config['alias_url'][link.page]) > 1:
                    log.error(f"{link} at '{ocurrence}' is ambiguous. It could be any of {config['alias_url'][link.page]}. Please add a path hint where the page is, e.g. [[A/B:page#anchor|text]].")
                if len(config['alias_url'][link.page]) == 1:
                    path = config['alias_url'][link.page][0]
                    md_link = link.to_markdown(path)
                    lines[i] = lines[i].replace(match.group(0), md_link)

            config['wikilinks'].add(link)

            if url_relative not in config['wikilinks_per_url']:
                config['wikilinks_per_url'][url_relative] = set()
            config['wikilinks_per_url'][url_relative].add(link)
    return '\n'.join(lines)

    # if current_page.file.src_path.endswith('dynamic-config-changed.md'):


# def on_files(files: Files, config: MkDocsConfig) -> None:
#     """When MkDocs loads its files, extract aliases from any Markdown files
#     that were found.
#     """


#     for file in filter(lambda f: f.is_documentation_page(), files):
#         with open(file.abs_src_path, encoding='utf-8-sig', errors='strict') as handle:
#             source, meta_data = meta.get_data(handle.read())
#             alias_names: Optional[List[str]] = _get_alias_names(meta_data)
#             if alias_names is None or len(alias_names) < 1:
#                 # _title:Optional[str] = _get_page_title(source, meta_data)
#                 # if _title and _title not in config['aliases']:
#                 #     _title = _title.strip()
#                 #     alias_names = [_title]
#                 #     meta_data['alias'] = { 'name': _title , 'text': _title }
#                 # else:
#                 continue

#             if len(alias_names) > 1:
#                 log.info(
#                     '%s defines %d aliases:', file.url, len(alias_names)
#                 )
#             for alias in alias_names:
#                 existing = config['aliases'].get(alias)
#                 if existing is not None:
#                     log.warning(
#                         "%s: alias %s already defined in %s, skipping.",
#                         file.src_uri,
#                         alias,
#                         existing['url']
#                     )
#                     continue

#                 new_alias = {
#                     'alias': alias,
#                     'text': (
#                         meta_data['alias']['text']
#                         # if meta_data['alias'] is a dictionary and 'text' is a key
#                         if isinstance(meta_data['alias'], dict) and \
#                         'text' in meta_data['alias']
#                         else _get_page_title(source, meta_data)
#                     ),
#                     'url': file.src_uri,
#                 }
#                 log.debug(
#                     "Alias '%s' to '%s'",
#                     alias,
#                     new_alias['url']
#                 )
#                 config['aliases'][alias] = new_alias

#     with open('docs/indexes/aliases.md', 'w') as f:
#         f.write(f"<h1>Aliases <small>({
#                 len(config['aliases'])})</small></h1>\n\n")
#         current_letter = ''
#         for_index = sorted(config['aliases'].keys()).copy()

#         if 'Aliases' in for_index:
#             for_index.remove('Aliases')

#         for alias in for_index:
#             if alias[0].upper() != current_letter:
#                 current_letter = alias[0].upper()
#                 f.write(f"\n## {current_letter}\n\n")
#             if 'http' in config['aliases'][alias]['url']:
#                 right_url = config['aliases'][alias]['url']
#             elif config['site_url'].endswith('nspec/'):
#                 right_url = f"{config['site_url'].rstrip(
#                     '/')}/{config['aliases'][alias]['url'].lstrip('./').replace('.md', '.html')}"
#             f.write(f"- [{alias}]({right_url})\n")
# # Helper functions


# def _get_page_title(page_src: str, meta_data: dict) -> Optional[str]:
#     """Returns the title of the page. The title in the meta data section
#     will take precedence over the H1 markdown title if both are provided."""
#     return (
#         meta_data['title']
#         if 'title' in meta_data and isinstance(meta_data['title'], str)
#         else get_markdown_title(page_src)
#     )


# def _get_alias_names(meta_data: dict):
#     """Returns the list of configured alias names."""
#     if len(meta_data) <= 0 or 'alias' not in meta_data:
#         # use_alias_first_
#         return None
#     aliases = meta_data['alias']
#     if isinstance(aliases, list):
#         # If the alias meta data is a list, ensure that they're strings
#         return list(filter(lambda value: isinstance(value, str), aliases))
#     if isinstance(aliases, dict) and 'name' in aliases:
#         return [aliases['name']]
#     if isinstance(aliases, str):
#         return [aliases]
#     return None

# def _replace_tag(
#     match: Match,
#     page_file: File,
#     config: MkDocsConfig
# ):

#     """Callback used in the sub function within on_page_markdown."""
#     if match.group(1) is not None:
#         # if the alias match was escaped, return the unescaped version
#         return match.group(0)[1:]
#     # split the tag up in case there's an anchor in the link
#     tag_bits = ['']
#     if match.group(2) is not None:
#         tag_bits = str(match.group(2)).strip().split('#')
#     if len(tag_bits) < 1:
#         log.warning(
#             "There is no anchor in the alias tag '%s' in '%s'",
#             match.group(2),
#             page_file.src_path)

#     # assume the aliases are stored in a dictionary in the config
#     alias = config['aliases'].get(tag_bits[0])

#     if alias is None:
#         config['num_alias_issues'] += 1
#         log.warning(
#             "Alias '%s' not found in '%s'",
#             match.group(2),
#             page_file.src_path
#         )
#         return match.group(0) # return the input string

#     text = alias['text'] if match.group(3) is None else match.group(3)
#     if text is None:
#         text = alias['url']

#     url = get_relative_url(alias['url'], page_file.src_uri)
#     if len(tag_bits) > 1:
#         url = f"{url}#{tag_bits[1]}"

#     config['num_uses_of_aliases'] += 1
#     log.info(
#         "replaced alias '%s' with '%s' to '%s'",
#         alias['alias'],
#         text,
#         url
#     )
#     return f"[{text}]({url})"


# a = FuzzyMap()
# a['test'] = '1'
# a['Worker'] = '2'
# a['Python Cookbook'] = '3'
# a['Clean Code'] = '4'
# a['The Pragmatic Programmer'] = '5'
# a['Design Patterns'] = '6'
# a['Code Complete'] = '7'
# a['Refactoring'] = '8'
# a['Effective Python'] = '9'
# a['The Clean Coder'] = '10'
# a['Cracking the Coding Interview'] = '11'

# print("++++++++++++++")

# if __name__ == '__main__':
#     # read from the input
#     while True:
#         key = input("Enter a key: ")
#         print(a[key])
