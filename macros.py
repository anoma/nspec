import json
import os
from datetime import datetime
from pathlib import Path

from mkdocs.structure.nav import Link, Navigation, Section
from mkdocs.structure.pages import Page

ROOT_DIR = Path(__file__).parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"

REPORT_BROKEN_WIKILINKS = bool(os.environ.get("REPORT_BROKEN_WIKILINKS", False))

PROCESS_JUVIX = bool(os.environ.get("PROCESS_JUVIX", False))

CACHE_DIR: Path = ROOT_DIR.joinpath(".cache-mkdocs-without-juvix-processing")
if PROCESS_JUVIX:
    CACHE_DIR = ROOT_DIR.joinpath(".cache-mkdocs-with-juvix-processing")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def load_json_file(file_path):
    if file_path.exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return {}


def define_env(env):
    env.variables.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    env.variables.preview = False
    env.variables.pull_request = False
    env.variables.pr_number = None

    SITE_DIR = os.environ.get("SITE_DIR", "")
    if SITE_DIR:
        if SITE_DIR.startswith("pull") or SITE_DIR.startswith("dev"):
            env.variables.preview = True
        if SITE_DIR.startswith("pull"):
            env.variables.pull_request = True
            env.variables.pr_number = SITE_DIR

    @env.macro
    def get_aliases():
        aliases_file = CACHE_DIR / "aliases.json"
        aliases_json = load_json_file(aliases_file)
        aliases = aliases_json.get("url_for", {})
        keys = sorted(list(aliases.keys()))
        aliases_by_letter = {}
        current_letter = None
        for alias in keys:
            letter = alias[0].upper()
            if letter != current_letter:
                current_letter = letter
                aliases_by_letter[current_letter] = []
            aliases_by_letter[current_letter].append(
                {"alias": alias, "url": aliases[alias]}
            )
        return aliases_by_letter

    @env.macro
    def get_juvix_modules():
        juvix_modules_file = CACHE_DIR / "juvix_modules.json"
        juvix_modules_by_letter = {}
        juvix_modules = load_json_file(juvix_modules_file)
        # filter out the ones that have no module_name
        juvix_modules = [mod for mod in juvix_modules if mod["module_name"]]
        juvix_modules = sorted(juvix_modules, key=lambda x: x["module_name"])
        current_letter = None
        for mod in juvix_modules:
            letter = mod["module_name"][0].upper()
            if letter != current_letter:
                current_letter = letter
                juvix_modules_by_letter[current_letter] = []
            juvix_modules_by_letter[current_letter].append(mod)
        return juvix_modules_by_letter

    @env.macro
    def date(d):
        return datetime.strptime(d, "%Y-%m-%d")

    @env.macro
    def type_of(x):
        return type(x).__name__

    @env.macro
    def nav_to_dict(nav):  # type: ignore
        if isinstance(nav, Navigation):
            return [nav_to_dict(section) for section in nav]
        if isinstance(nav, Section):
            url = None
            # here we assume the mkdocs.plugins section_index plugin is used
            children = list(map(nav_to_dict, nav.children))
            if len(children) >= 1:
                if children[0].get("url") and children[0]["url"].endswith("index.md"):
                    url = children[0]["url"]
                    children = children[1:]
            return {
                "title": nav.title,
                "url": url,
                "children": children,
            }
        if isinstance(nav, Link):
            return {"title": nav.title, "url": nav.url}
        if isinstance(nav, Page):
            url = nav.url
            if not url.startswith("./") and not url.startswith("http"):
                url = f"./{url}"
                if url.endswith(".html"):
                    url = url.replace(".html", ".md")
            return {"title": nav.title, "url": str(url)}
        return nav

    @env.macro
    def tutorial_for_contributors(navigation):
        nav_dict = nav_to_dict(navigation)
        list_md = []
        for dict in nav_dict:
            if dict and "title" in dict and dict["title"] == "Tutorials for contributors":  # type: ignore
                for chapter in dict["children"]:  # type: ignore
                    list_md.append(f"- [{chapter['title']}]({chapter['url']})\n")  # type: ignore
        return "\n".join(list_md)

    @env.macro
    def dict_to_md(nav_dict, depth=0) -> str:
        if isinstance(nav_dict, list):
            return "\n\n".join(dict_to_md(section, depth) for section in nav_dict)
        indented_prefix = f"{'  ' * depth}- "
        if isinstance(nav_dict, dict):
            if "title" in nav_dict:
                title = nav_dict["title"]
                if "ToC" == title:
                    title = "Table of Contents"
                if "url" in nav_dict and nav_dict["url"]:
                    item_md = (
                        f"{indented_prefix}[{nav_dict['title']}]({nav_dict['url']})"
                    )
                else:
                    item_md = f"{indented_prefix}{nav_dict['title']}"
                if "children" in nav_dict:
                    children_md = dict_to_md(nav_dict["children"], depth + 1)
                    return f"{item_md}\n{children_md}"
                return item_md
        return f"{indented_prefix}{nav_dict}"


def on_pre_page_macros(env):
    """
    Actions to be performed before the page macros are expanded.
    """
    pass

def on_post_page_macros(env):
    """
    Actions to be performed after the page macros have been expanded.
    """
    pass
