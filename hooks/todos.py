
import re
import os
import logging
from pathlib import Path
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files
from mkdocs.config.defaults import MkDocsConfig
from markdown.preprocessors import Preprocessor  # type: ignore
from markdown.extensions import Extension  # type: ignore

log: logging.Logger = logging.getLogger('mkdocs')

ROOT_DIR = Path(__file__).parent.parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"

REMOVE_TODOS = bool(os.environ.get('REMOVE_TODOS', False))
REPORT_TODOS = bool(os.environ.get('REPORT_TODOS', False))

IMAGES_PATTERN = re.compile(r"""
\s+!!!\s+todo\s+(?P<title>.+)
""", re.VERBOSE)

class TodoOcurrence:
    def __init__(self, file:str, line:int, col:int, message:str = ""):
        self.file = file
        self.line = line
        self.col = col
        self.message = message

    def __str__(self):
        short_msg = self.message[:100] + "..." if len(self.message) > 100 else self.message
        return f"\033[92m{self.file}\033[0m:{self.line}:{self.col} \n - {short_msg}"

    def __repr__(self):
        return self.__str__()

class RTExtension(Extension):

    def __init__(self, mkconfig):
        self.mkconfig = mkconfig

    def extendMarkdown(self, md):  # noqa: N802

        self.md = md
        md.registerExtension(self)

        self.imgpp = RTPreprocessor(self.mkconfig)
        md.preprocessors.register(self.imgpp, 'todo-pp', 120)

class RTPreprocessor(Preprocessor):

    def __init__(self, mkconfig):
        self.mkconfig = mkconfig

    def run(self, lines):

        config = self.mkconfig
        current_page_url = None

        if 'current_page' in config \
                and isinstance(config['current_page'], Page):
            url_relative = DOCS_DIR / \
                Path(config['current_page'].url.replace('.html', '.md'))
            current_page_url = url_relative.as_posix()

        final_lines = []
        num_todo_entries = 0
        I = 0
        while I < len(lines):
            line = lines[I]
            if line.strip().startswith("!!! todo"):
                num_todo_entries += 1
                _line = line.lstrip()
                nwspaces = len(line) - len(_line)
                message = ""
                for J in range(I+1, len(lines)):
                    if len(lines[J].strip()) == 0:
                        continue
                    if lines[J].startswith(' '* nwspaces):
                        message += lines[J].strip()
                    else:
                        break  
                todo = TodoOcurrence(current_page_url, I, nwspaces, message)
                if REPORT_TODOS:
                    log.warning(todo)
                I = J
            else:
                final_lines.append(line)
            I += 1
        return final_lines if REMOVE_TODOS else lines

def on_config(config: MkDocsConfig, **kwargs) -> MkDocsConfig:
    config.markdown_extensions.append(RTExtension(config))
    return config

def on_page_markdown(markdown, page: Page, config: MkDocsConfig, files: Files) -> str:
    config['current_page'] = page  # needed for the preprocessor
    return markdown
