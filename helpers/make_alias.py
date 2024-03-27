
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
from fuzzywuzzy import fuzz # type: ignore

log: logging.Logger = logging.getLogger('mkdocs')

INDEXES_DIR = Path('docs/indexes')
INDEXES_DIR.mkdir(parents=True, exist_ok=True)


""" Example of a wikilink:
[[path-hint:page#anchor|display text]]
"""

WIKILINK_PATTERN = re.compile(r"""
    \[\[                          # Opening brackets
    (?P<hint>(?:[^\]|#\n]+/)*?)   # Optional hint path, non-greedy
    (?P<page>[^\]|#\n]+?)         # Page name, excluding closing brackets, pipe, hash for anchors, and newlines, non-greedy
    (?:                           # Non-capturing group for optional sections
        #                         # Hash for anchors
        (?P<anchor>[^\]|\n]+)     # Anchor text, excluding closing brackets and newlines
    )?                            # Anchor is optional
    (?:                           # Non-capturing group for optional display text
        \|                        # Pipe separating page/anchor from display text
        (?P<display>[^\]\n]+)     # Display text, excluding closing brackets and newlines
    )?                            # Display text is optional
    \]\]                          # Closing brackets
""", re.VERBOSE | re.DOTALL)

class WikiLink:
    def __init__(self, page: str, hint: Optional[str] = None, anchor: Optional[str] = None, display: Optional[str] = None):
        self.page: str = page.strip()
        self.hint: Optional[str] = hint.strip() if hint else None
        self.anchor: Optional[str] = anchor.strip(
        )[1:] if anchor and anchor.startswith('#') else None
        self.display: Optional[str] = display.strip() if display else None
        self.references: List[Any] = []

    def __str__(self):
        link = f"[[{self.hint}:{self.page}"
        if self.anchor:
            link += f"#{self.anchor}"
        if self.display:
            link += f"|{self.display}"
        link += "]]"
        return link

    def __hash__(self):
        return hash(self.page)

    def __repr__(self):
        return f"WikiLink(alias={self.page}, hint={self.hint}, anchor={self.anchor}, display={self.display})"

    def to_markdown(self):
        return f"[{self.display or self.page}]({self.hint}:{self.page}{f'#{self.anchor}' if self.anchor else ''})"

    def add_reference(self, page: Any):
        self.references.append(page)

    def references_to_list_markdown(self):
        return '\n'.join([f"- {page}" for page in self.references])

# ------------------------------------------------------------------------------
# The generation of the graph of links and cross-references is only based on the
# navigation structure of the site. This is a limitation of the current version
# of the plugin. The reason is that we run this routin before the (real) build
# starts, as we later add content at the end of each markdown file, in case it
# is mentioned somewhere by a wikilink.

def on_pre_build(config: MkDocsConfig):
    """Executed before the build begins. Initializes the aliases dictionary
    and the alias issue and alias use counters.
    """
    with open(INDEXES_DIR / 'aliases.md', 'w') as f:
        f.write("# Aliases\n\n")

    # a graph where the nodes are the pages (src_path) and the edges are
    # determined by the (wikilinks) references, initially.
        
    config['wiklink_graph'] = {}
    config['url_alias'] = {}
    config['alias_url'] = {}

    for url, page_alias in _extract_aliases_from_nav(config['nav']):
        config['url_alias'][url] = [page_alias]
        if not page_alias in config['alias_url']:
            config['alias_url'][page_alias] = [url]
        else:
            config['alias_url'][page_alias].append(url)

    # print(config['url_alias'])
    # print("-----")
    # with open(".dict", 'w') as f:
    #     for k, v in config['alias_url'].items():
    #         f.write(f"{k} -> {v}\n")
    # print("-----")
    # while True:
    #     key = input("Enter a key: ")
    #     if key in config['alias_url']:
    #         print(config['alias_url'][key])
    #         results = config['alias_url'][key]
    #         # use fuzzy matching to find the closest element in the list
    #         # given a hint
    #         if len(results) >1:
    #             hint = input("Enter a hint: ")
    #             coefficients = {k: fuzz.WRatio(k, hint) for k in results}
    #             n = len(results)
    #             result = sorted(coefficients, key=lambda k: coefficients[k], reverse=True)[:n]
    #             keypairs = [(k, coefficients[k]) 
    #                         for k in result]
    #             for k, v in keypairs:
    #                 print(f"{k} -> {v}")
        # print("Possible matches: Add hint to disembiguate")
        # for k in config['alias_url'].get_k_closest(key, 5):
        #     print(k)
    # exit()


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

def _get_aliases_from_nav(config: MkDocsConfig) -> MkDocsConfig:

    paths_in_nav:List[Tuple[str, str]] = []

    print(_extract_aliases_from_nav(config['nav']))
    print(len(_extract_aliases_from_nav(config['nav'])))
    print(len(set(_extract_aliases_from_nav(config['nav']))))

    # for t, p in process_item(config['nav']).items():
    #     config['alias']['by_url'][p] = \
    #         config['alias']['by_title'].setdefault(p, []).append(t)
    #     config['alias']['by_title'][t] = p

    # print(config['alias']['by_url'])
    # print(paths_in_nav)
    # check if paths_in_nav has any duplicates using the second element

    exit()

# def on_post_build(config: MkDocsConfig):
#     aliases_dict = config.get('aliases', {})
#     num_alias_issues = config.get('num_alias_issues', 0)
#     num_uses_of_aliases = config.get('num_uses_of_aliases', 0)

#     log.info("Defined %s alias(es).", len(aliases_dict))
#     log.info("Found %s alias issue(s).", num_alias_issues)
#     log.info("Used %s alias(es).", num_uses_of_aliases)
#     aliases_dict.clear()


# def on_page_markdown(markdown: str, *, page: Page, config: MkDocsConfig, **_) -> str:
#     """Replaces any alias tags on the page with markdown links."""
#     current_page = page
#     print("current_page: ", current_page.file.src_path)

#     matches = WIKILINK_PATTERN.finditer(markdown)

#     if current_page.file.src_path.endswith('dynamic-config-changed.md'):
#         print("current_page: ", current_page.file.src_path)

#         for match in matches:
#             wikilink = WikiLink(
#                 alias=match.group('page'),
#                 anchor=match.group('anchor'),
#                 display=match.group('display')
#             )
#             print(wikilink)
#         exit()
#     return ""

#     # return re.sub(
#     #     ALIAS_TAG_REGEX,
#     #     lambda match: _replace_tag(
#     #         match,
#     #         current_page.file,
#     #         config
#     #     ),
#     #     markdown,
#     #     count=0,
#     #     flags=re.MULTILINE
#     # )


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


