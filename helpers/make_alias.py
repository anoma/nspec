
"""
Based on the mkdocs-alias-plugin's implementation. The main difference is that
this implementation uses the title as an alias if no alias is defined in the
meta data.

TODO: 
[[Link#anchor|Link Title]]) is not supported.
"""

from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.utils import meta, get_markdown_title, get_relative_url
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple
from typing import Match
import logging
import re

log: logging.Logger = logging.getLogger('mkdocs')

# The Regular Expression used to find alias tags
ALIAS_TAG_REGEX = r"([\\])?\[\[([^|\]]+)\|?([^\]]+)?\]\]"

from fuzzywuzzy import fuzz # type: ignore

class FuzzyMap(dict):
    ratio = 80

    def closest_key(self, key):
        """Returns the closest key matched by the given ratio"""
        # print("len(self): ", len(self))
        # print("self.keys(): ", self.keys())
        # print("key: ", key)
        # print("--------------------")
        if len(self):

            # Calculate matching coefficient of each key via fuzz.ratio
            coefficients = {k: fuzz.UWRatio(k, key) for k in self.keys()}
            matching = max(coefficients, key=lambda k: coefficients[k])
            # print("coefficients: ", coefficients)
            # print("matching: ", matching)
            if coefficients[matching] >= self.ratio:
                return matching
        return key

    def get(self, key, default=None):
        return self[key] or default

    def __missing__(self, key):
        return super().get(self.closest_key(key))

    def __setitem__(self, key, value):
        super().__setitem__(self.closest_key(key), value)



def on_pre_build(config: MkDocsConfig):
    """Executed before the build begins. Initializes the aliases dictionary
    and the alias issue and alias use counters.
    """
    Path('docs/indexes').mkdir(parents=True, exist_ok=True)
    # create the alias file if it doesn't exist
    with open('docs/indexes/aliases.md', 'w') as f:
        f.write("# Aliases\n\n")

    config['aliases'] = FuzzyMap()
    config['num_alias_issues'] = 0
    config['num_uses_of_aliases'] = 0

def on_post_build(config : MkDocsConfig):
    aliases_dict = config.get('aliases', {})
    num_alias_issues = config.get('num_alias_issues', 0)
    num_uses_of_aliases = config.get('num_uses_of_aliases', 0)
    log.info("Defined %s alias(es).", len(aliases_dict))
    log.info("Found %s alias issue(s).", num_alias_issues)
    log.info("Used %s alias(es).", num_uses_of_aliases)
    aliases_dict.clear()

def on_page_markdown(markdown: str, *, page, config: MkDocsConfig, **_) -> str:
    """Replaces any alias tags on the page with markdown links."""
    current_page = page
    return re.sub(
        ALIAS_TAG_REGEX,
        lambda match: _replace_tag(
            match,
            current_page.file,
            config
        ),
        markdown
    )

def on_files(files, config: MkDocsConfig) -> None:
    """When MkDocs loads its files, extract aliases from any Markdown files
    that were found.
    """
    for file in filter(lambda f: f.is_documentation_page(), files):
        with open(file.abs_src_path, encoding='utf-8-sig', errors='strict') as handle:
            source, meta_data = meta.get_data(handle.read())
            alias_names : Optional[List[str]] = _get_alias_names(meta_data)
            if alias_names is None or len(alias_names) < 1:
                _title:Optional[str] = _get_page_title(source, meta_data)
                if _title and _title not in config['aliases']:
                    _title = _title.strip()
                    alias_names = [_title]
                    meta_data['alias'] = { 'name': _title , 'text': _title }
                else:
                    continue

            if len(alias_names) > 1:
                log.info(
                    '%s defines %d aliases:', file.url, len(alias_names)
                )
            for alias in alias_names:
                existing = config['aliases'].get(alias)
                if existing is not None:
                    log.warning(
                        "%s: alias %s already defined in %s, skipping.",
                        file.src_uri,
                        alias,
                        existing['url']
                    )
                    continue

                new_alias = {
                    'alias': alias,
                    'text': (
                        meta_data['alias']['text']
                        # if meta_data['alias'] is a dictionary and 'text' is a key
                        if isinstance(meta_data['alias'], dict) and \
                            'text' in meta_data['alias']
                        else _get_page_title(source, meta_data)
                    ),
                    'url': file.src_uri,
                }
                log.debug(
                    "Alias '%s' to '%s'",
                    alias,
                    new_alias['url']
                )
                config['aliases'][alias] = new_alias

    with open('docs/indexes/aliases.md', 'w') as f:
        f.write(f"<h1>Aliases <small>({len(config['aliases'])})</small></h1>\n\n")
        current_letter = ''
        for_index = sorted(config['aliases'].keys()).copy()
        for_index.remove('Aliases')
        for alias in for_index:
            if alias[0].upper() != current_letter:
                current_letter = alias[0].upper()
                f.write(f"## {current_letter}\n\n")
            f.write(f"- [{alias}](/{config['aliases'][alias]['url'].replace('.md', '.html')})\n")
# Helper functions
                
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
        # use_alias_first_
        return None
    aliases = meta_data['alias']
    if isinstance(aliases, list):
        # If the alias meta data is a list, ensure that they're strings
        return list(filter(lambda value: isinstance(value, str), aliases))
    if isinstance(aliases, dict) and 'name' in aliases:
        return [ aliases['name'] ]
    if isinstance(aliases, str):
        return [ aliases ]
    return None

def _replace_tag(
    match: Match,
    page_file: File,
    config: MkDocsConfig
):
    
    """Callback used in the sub function within on_page_markdown."""
    if match.group(1) is not None:
        # if the alias match was escaped, return the unescaped version
        return match.group(0)[1:]
    # split the tag up in case there's an anchor in the link
    tag_bits = ['']
    if match.group(2) is not None:
        tag_bits = str(match.group(2)).strip().split('#')
    if len(tag_bits) < 1:
        log.warning(
            "There is no anchor in the alias tag '%s' in '%s'",
            match.group(2),
            page_file.src_path)
    
    # assume the aliases are stored in a dictionary in the config
    alias = config['aliases'].get(tag_bits[0])

    if alias is None:
        config['num_alias_issues'] += 1
        log.warning(
            "Alias '%s' not found in '%s'",
            match.group(2),
            page_file.src_path
        )
        return match.group(0) # return the input string

    text = alias['text'] if match.group(3) is None else match.group(3)
    if text is None:
        text = alias['url']

    url = get_relative_url(alias['url'], page_file.src_uri)
    if len(tag_bits) > 1:
        url = f"{url}#{tag_bits[1]}"

    config['num_uses_of_aliases'] += 1
    log.debug(
        "replaced alias '%s' with '%s' to '%s'",
        alias['alias'],
        text,
        url
    )
    return f"[{text}]({url})"
    

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