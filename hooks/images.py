import re
import os
import shutil
import subprocess
import logging
from pathlib import Path
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files
from mkdocs.config.defaults import MkDocsConfig
from markdown.preprocessors import Preprocessor  # type: ignore
from markdown.extensions import Extension  # type: ignore
from common.utils import fix_url
from common.models.fileloc import FileLoc

log: logging.Logger = logging.getLogger("mkdocs")

INDEXES_DIR = Path("docs/indexes")
INDEXES_DIR.mkdir(parents=True, exist_ok=True)

ROOT_URL = "/nspec/"
ROOT_DIR = Path(__file__).parent.parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"
IMAGES_DIR = DOCS_DIR / "images"

CACHE_DIR: Path = ROOT_DIR.joinpath(".hooks")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

CACHE_IMAGES = CACHE_DIR / ".images"
CACHE_IMAGES.mkdir(parents=True, exist_ok=True)

IMAGES_PATTERN = re.compile(
    r"""
!\[
(?P<caption>[^\]]*)\]\(
(?P<url>[^\)]+)\)
""",
    re.VERBOSE,
)


DOT_BIN = os.getenv("DOT_BIN", "dot")
USE_DOT = bool(os.getenv("USE_DOT", True))

if not shutil.which(DOT_BIN):
    log.error(
        f"Graphviz not found. Please install it and set the DOT_BIN environment variable."
    )
    USE_DOT = False


class ImgExtension(Extension):

    def __init__(self, mkconfig: MkDocsConfig):
        self.mkconfig = mkconfig

    def __repr__(self):
        return "ImgExtension"

    def extendMarkdown(self, md):  # noqa: N802

        self.md = md
        md.registerExtension(self)

        self.imgpp = ImgPreprocessor(self.mkconfig)
        md.preprocessors.register(self.imgpp, "img-pp", 110)


def on_config(config: MkDocsConfig, **kwargs) -> MkDocsConfig:
    imgext_instance = ImgExtension(mkconfig=config)
    config.markdown_extensions.append(imgext_instance)  # type: ignore

    config["images"] = {}  # page: [image]
    config.setdefault("current_page", None)  # current page being processed
    config["images_issues"] = 0
    return config


class ImgPreprocessor(Preprocessor):

    def __init__(self, mkconfig):
        self.mkconfig = mkconfig

    def run(self, lines):

        config = self.mkconfig
        current_page_url = None

        if "current_page" in config and isinstance(config["current_page"], Page):
            url_relative = DOCS_DIR / Path(
                config["current_page"].url.replace(".html", ".md")
            )
            current_page_url = url_relative.as_posix()

        if not current_page_url:
            log.error("Current page URL not found. Images will not be processed.")
            return lines

        in_html_comment = False
        in_div = False

        for i, line in enumerate(lines.copy()):
            if "<!--" in line:
                in_html_comment = True
            if "-->" in line:
                in_html_comment = False
            if "<div" in line:
                in_div = True
            if "</div>" in line:
                in_div = False
            if in_html_comment or in_div:
                continue

            matches = IMAGES_PATTERN.finditer(line)

            for match in matches:
                _url = match.group("url")
                url = Path(_url)
                if url.as_posix().startswith("http"):
                    continue

                loc = FileLoc(current_page_url, i + 1, match.start() + 2)

                image_fname = url.name
                img_cache = CACHE_IMAGES / image_fname

                if not CACHE_IMAGES.exists():
                    CACHE_IMAGES.mkdir(parents=True, exist_ok=True)

                if image_fname.endswith(".dot.svg") and USE_DOT:
                    dot_file = image_fname.replace(".dot.svg", ".dot")
                    dot_location = IMAGES_DIR / dot_file
                    log.debug(f"{loc}\nGenerating SVG from DOT file: {dot_location}")

                    if not dot_location.exists():
                        log.info(f"{dot_location} not found. Skipping SVG generation.")
                        continue

                    cmd = f"{DOT_BIN} -Tsvg {dot_location.as_posix()} -o {img_cache.absolute().as_posix()}"

                    log.debug(f"Running command: {cmd}")

                    output = subprocess.run(cmd, shell=True, check=True)

                    if output.returncode != 0:
                        log.error(f"Error running graphviz: {output}")

                    if not img_cache.exists():
                        config["images_issues"] += 1
                        log.error(
                            f"{loc}\n [!] Image not found. Expected location:\n==> {img_cache}"
                        )

                img_expected_location = IMAGES_DIR / image_fname
                new_url = fix_url(
                    root=config["site_url"],
                    url=img_expected_location.relative_to(DOCS_DIR).as_posix(),
                    html=True,
                )

                lines[i] = lines[i].replace(_url, new_url)

                log.debug(
                    f"{loc}\n[!] Image URL: {_url}\nwas replaced by the following URL:\n ==> {new_url}"
                )
        return lines


def on_page_markdown(markdown, page: Page, config: MkDocsConfig, files: Files) -> str:
    config["current_page"] = page  # needed for the preprocessor
    return markdown


def on_post_build(config: MkDocsConfig) -> None:
    if config["images_issues"] > 0:
        log.error(
            f"\n[!] {config['images_issues']} image(s) not found. Please check the logs for more details."
        )
    else:
        site_dir = config.get("site_dir", "site")
        shutil.copytree(CACHE_IMAGES, Path(site_dir) / "images", dirs_exist_ok=True)
