
"""
Based on the mkdocs-alias-plugin's implementation. The main difference is that
this implementation uses the title as an alias if no alias is defined in the
meta data.

TODO: 
[[Link#anchor|Link Title]]) is not supported.
"""

from mkdocs.config import config_options
from mkdocs.structure.files import File
from mkdocs.structure.files import Files
from mkdocs.utils import meta, get_markdown_title, get_relative_url
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple
from typing import Match
import logging
import os
import re


log: logging.Logger = logging.getLogger('mkdocs')

# The Regular Expression used to find alias tags
ALIAS_TAG_REGEX = r"([\\])?\[\[([^|\]]+)\|?([^\]]+)?\]\]"
aliases: Any  = {}
current_page:Any = None
num_alias_issues: int = 0
num_uses_of_aliases: int = 0

def on_post_build(**_):
    """Executed after the build has completed. Clears the aliases from
    memory and displays stats if the verbose option is configured.
    """
    log.info("Defined %s alias(es).", len(aliases))
    log.info("Found %s alias issue(s).", num_alias_issues)
    log.info("Used %s alias(es).", num_uses_of_aliases)
    aliases.clear()

def on_page_markdown(markdown: str, *, page, **_):
    """Replaces any alias tags on the page with markdown links."""
    current_page = page
    return re.sub(
        ALIAS_TAG_REGEX,
        lambda match: _replace_tag(
            match,
            aliases,
            current_page.file
        ),
        markdown
    )

def on_files(files, **_) -> None:
    """When MkDocs loads its files, extract aliases from any Markdown files
    that were found.
    """
    for file in filter(lambda f: f.is_documentation_page(), files):
        with open(file.abs_src_path, encoding='utf-8-sig', errors='strict') as handle:
            source, meta_data = meta.get_data(handle.read())
            alias_names : Optional[List[str]] = _get_alias_names(meta_data)
            if alias_names is None or len(alias_names) < 1:
                _title:Optional[str] = _get_page_title(source, meta_data)
                if _title and _title not in aliases:
                    _title = _title.strip()
                    alias_names = [_title]
                    meta_data['alias'] = { 'name': _title }
                else:
                    continue

            if len(alias_names) > 1:
                log.info(
                    '%s defines %d aliases:', file.url, len(alias_names)
                )
            for alias in alias_names:
                existing = aliases.get(alias)
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
                log.info(
                    "Alias %s to %s",
                    alias,
                    new_alias['url']
                )
                aliases[alias] = new_alias


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
    aliases: dict,
    page_file: File
):
    global num_alias_issues
    global num_uses_of_aliases
    
    """Callback used in the sub function within on_page_markdown."""
    if match.group(1) is not None:
        # if the alias match was escaped, return the unescaped version
        return match.group(0)[1:]
    # split the tag up in case there's an anchor in the link
    tag_bits = ['']
    if match.group(2) is not None:
        tag_bits = str(match.group(2)).split('#')
    alias = aliases.get(tag_bits[0])
    if alias is None:
        num_alias_issues += 1
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

    num_uses_of_aliases += 1
    log.debug(
        "replaced alias '%s' with '%s' to '%s'",
        alias['alias'],
        text,
        url
    )
    return f"[{text}]({url})"