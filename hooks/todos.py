"""
This plugin is used to find and report TODOs in the documentation.
"""

import logging
import os
from pathlib import Path
from typing import List

from common.models.loc import FileLoc as Todo
from markdown.extensions import Extension  # type: ignore
from markdown.preprocessors import Preprocessor  # type: ignore
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

log: logging.Logger = logging.getLogger("mkdocs")

ROOT_DIR = Path(__file__).parent.parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"

SHOW_TODOS_IN_MD = bool(os.environ.get("SHOW_TODOS_IN_MD", False))
REPORT_TODOS = bool(os.environ.get("REPORT_TODOS", False))


class RTExtension(Extension):
    def __repr__(self):
        return "RTExtension"

    def __init__(self, mkconfig):
        self.mkconfig = mkconfig

    def extendMarkdown(self, md):  # noqa: N802
        self.md = md
        md.registerExtension(self)

        self.imgpp = RTPreprocessor(self.mkconfig)
        md.preprocessors.register(self.imgpp, "todo-pp", 90)


class RTPreprocessor(Preprocessor):
    def __init__(self, mkconfig: MkDocsConfig):
        self.mkconfig = mkconfig

    def run(self, lines: List[str]) -> List[str]:
        config = self.mkconfig
        current_page_url = None
        preprocess_page = SHOW_TODOS_IN_MD

        if "current_page" in config and isinstance(config["current_page"], Page):
            url_relative = DOCS_DIR / Path(
                config["current_page"].url.replace(".html", ".md")
            )
            current_page_url = url_relative.as_posix()
            current_page_abs = config["current_page"].file.abs_src_path

            if "todos" in config["current_page"].meta:
                preprocess_page = bool(config["current_page"].meta["todos"])

        if not preprocess_page:
            return lines

        without_todos = []

        offset = 1
        with open(current_page_abs, "r") as f:
            first_line = f.readline()
            if first_line.startswith("---"):
                while f.readline().strip() != "---":
                    offset += 1
                offset += 1

        I = 0
        while I < len(lines):
            line = lines[I]
            if line.strip().startswith("!!! todo"):
                message = ""
                in_message = False
                I += 1
                ROW = I
                while I < len(lines):
                    s = lines[I]
                    if in_message:
                        if len(s.strip()) > 0:
                            message += s + "\n"
                        else:
                            break
                    elif len(s.strip()) == 0:
                        in_message = True
                    I += 1

                if current_page_url:
                    todo = Todo(
                        path=current_page_url,
                        line=ROW + offset + 1,
                        column=0,
                        text=message,
                    )
                    if REPORT_TODOS:
                        log.warning(todo)
            else:
                without_todos.append(line)
            I += 1

        return lines if SHOW_TODOS_IN_MD else without_todos


def on_config(config: MkDocsConfig, **kwargs) -> MkDocsConfig:
    rt_extension = RTExtension(config)
    config.markdown_extensions.append(rt_extension)  # type: ignore
    return config


def on_page_markdown(markdown, page: Page, config: MkDocsConfig, files: Files) -> str:
    config["current_page"] = page  # needed for the preprocessor
    return markdown
