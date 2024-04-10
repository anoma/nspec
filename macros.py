from datetime import datetime
import os
from pathlib import Path
import logging
import json

INDEXES_DIR = Path("docs/indexes")
INDEXES_DIR.mkdir(parents=True, exist_ok=True)

ROOT_DIR = Path(__file__).parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"

SITE_URL = os.environ.get("SITE_URL", "/nspec/")
REPORT_BROKEN_WIKILINKS = bool(os.environ.get("REPORT_BROKEN_WIKILINKS", False))

CACHE_DIR: Path = ROOT_DIR.joinpath(".hooks")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

log = logging.getLogger("mkdocs")


def load_json_file(file_path):
    if file_path.exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return {}


def define_env(env):
    env.variables.version = "v2"
    env.variables.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate the list of aliases by letter

    aliases_file = CACHE_DIR / "aliases.json"
    env.variables.aliases_by_letter = {}
    aliases_json = load_json_file(aliases_file)
    aliases = aliases_json.get("url_for", {})
    keys = sorted(list(aliases.keys()))
    current_letter = None
    for alias in keys:
        letter = alias[0].upper()
        if letter != current_letter:
            current_letter = letter
            env.variables.aliases_by_letter[current_letter] = []
        env.variables.aliases_by_letter[current_letter].append(
            {"alias": alias, "url": aliases[alias]}
        )

    # Generate the list of Juvix modules by letter

    juvix_modules_file = CACHE_DIR / "juvix_modules.json"
    env.variables.juvix_modules_by_letter = {}
    env.variables.juvix_modules = load_json_file(juvix_modules_file)
    sorted(env.variables.juvix_modules, key=lambda x: x["module_name"])
    current_letter = None
    for mod in env.variables.juvix_modules:
        letter = mod["module_name"][0].upper()
        if letter != current_letter:
            current_letter = letter
            env.variables.juvix_modules_by_letter[current_letter] = []
        env.variables.juvix_modules_by_letter[current_letter].append(mod)

    @env.macro
    def date(d):
        return datetime.strptime(d, "%Y-%m-%d")


def on_pre_page_macros(env):
    """
    Actions to be performed before the page macros are expanded.
    """
    env.markdown += f"<!-- Last updated: {env.variables.last_updated} -->"


def on_post_page_macros(env):
    """
    Actions to be performed after the page macros have been expanded.
    """
    pass
