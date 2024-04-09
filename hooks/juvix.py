"""
This hook here is used to render Juvix clickable links in the markdown files.
"""

from functools import lru_cache
import logging
import os
import shutil
import subprocess
import hashlib
from pathlib import Path
import time
from typing import Any, Callable, List, Optional, Tuple

import pathspec
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from watchdog.events import FileSystemEvent

from common.utils import fix_url
from common.cache import compute_sha_over_folder, hash_file, hash_file_hash_obj

log: logging.Logger = logging.getLogger("mkdocs")

PREPROCESS_JUVIX_MD = bool(os.environ.get("JUVIX_SUPPORT", True))

ROOT_URL = "/nspec/"
ROOT_DIR: Path = Path(__file__).parent.parent.absolute()
DOCS_DIR: Path = ROOT_DIR.joinpath("docs")

IGNORE_CACHE = bool(os.environ.get("IGNORE_CACHE", False))
CACHE_HOOKS: Path = ROOT_DIR.joinpath(".hooks")
CACHE_HOOKS.mkdir(parents=True, exist_ok=True)

MARKDOWN_JUVIX_OUTPUT: Path = CACHE_HOOKS.joinpath(".md")
MARKDOWN_JUVIX_OUTPUT.mkdir(parents=True, exist_ok=True)

JUVIX_BIN: str = os.environ.get("JUVIX_BIN", "juvix")
JUVIX_AVAILABLE = shutil.which(JUVIX_BIN) is not None
JUVIX_VERSION: Optional[str] = None

if JUVIX_AVAILABLE:
    cmd = [JUVIX_BIN, "--numeric-version"]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        JUVIX_VERSION = result.stdout.decode("utf-8")
        log.info(f"Using Juvix v{JUVIX_VERSION} to render Juvix Markdown files.")

JUVIXCODE_CACHE_DIR: Path = CACHE_HOOKS.joinpath(".juvix_md")
JUVIXCODE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
JUVIXCODE_HASH_FILE = CACHE_HOOKS.joinpath(".hash_juvix_md")

HASH_DIR: Path = CACHE_HOOKS.joinpath(".hash")
HASH_DIR.mkdir(parents=True, exist_ok=True)

HTML_CACHE_DIR: Path = CACHE_HOOKS.joinpath(".html")

# The following prevents to build html every time
# a .juvix.md file changes.
FAST = bool(int(os.environ.get("FAST", True)))

try:
    subprocess.run([JUVIX_BIN, "--version"], capture_output=True)
except FileNotFoundError:
    log.warning(
        "The Juvix binary is not available. Please install Juvix and make sure it's available in the PATH."
    )


def on_config(config) -> None:
    """
    This runs before the build process begins. It is used to generate the Juvix
    markdown files and the corresponding HTML files. We need to isoloate all the
    .juvix.md files to compute a more effective hash. How? copy all the
    .juvix.md files to JUVIXCODE_CACHE_DIR, respecting the folder structure.
    Compute the SHA hash over the JUVIXCODE_CACHE_DIR folder and save it to
    JUVIXCODE_HASH_FILE. Generate the HTML Juvix project using the provided
    config.
    """

    if not PREPROCESS_JUVIX_MD or not JUVIX_AVAILABLE:
        return

    try:
        subprocess.run([JUVIX_BIN, "dependencies", "update"], capture_output=True)
    except Exception as e:
        log.error(f"Juvix error: {e}")
        return

    juvix = JuvixPreprocessor(mkconfig=config)
    for _file in DOCS_DIR.rglob("*.juvix.md"):
        file: Path = _file.absolute()
        juvix.generate_markdown(file)
    _hash: str = compute_sha_over_folder(JUVIXCODE_CACHE_DIR)
    with open(JUVIXCODE_HASH_FILE, "w") as f:
        f.write(_hash)
    juvix._html_juvix_project(generate=True)
    return


def on_files(files: Files, *, config: MkDocsConfig) -> Optional[Files]:
    for file in files:
        if ".juvix-build" in file.abs_src_path:
            files.remove(file)
    return files


def on_page_read_source(page: Page, config: MkDocsConfig) -> Optional[str]:
    filepath = Path(page.file.abs_src_path)
    juvix = JuvixPreprocessor(config)
    if (
        PREPROCESS_JUVIX_MD
        and filepath.as_posix().endswith(".juvix.md")
        and JUVIX_AVAILABLE
        and (output := juvix.generate_markdown(filepath))
    ):
        return output
    return page.content


def on_post_build(config: MkDocsConfig) -> None:
    juvix = JuvixPreprocessor(config)
    juvix.build_aux_html()
    return


def on_startup(command, dirty):
    if IGNORE_CACHE:
        shutil.rmtree(CACHE_HOOKS, ignore_errors=True)
        CACHE_HOOKS.mkdir(parents=True, exist_ok=True)
    return


def on_serve(server: Any, config: MkDocsConfig, builder: Any) -> None:

    gitignore = None

    with open(ROOT_DIR / ".gitignore") as file:
        gitignore = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern, file  # type: ignore
        )

    def callback_wrapper(
        callback: Callable[[FileSystemEvent], None]
    ) -> Callable[[FileSystemEvent], None]:
        def wrapper(event: FileSystemEvent) -> None:
            if gitignore.match_file(
                Path(event.src_path).relative_to(config.docs_dir).as_posix()
            ):
                return
            fpath: Path = Path(event.src_path).absolute()
            fpathstr: str = fpath.as_posix()

            if ".juvix-build" in fpathstr:
                return

            if fpathstr.endswith(".juvix.md"):
                log.debug("Juvix file changed: %s", fpathstr)
                log.debug(
                    "Hyperlinks to Juvix code external to the docs folder will not work. Only in the build mode they will generate."
                )
            return callback(event)

        return wrapper

    handler = (
        next(
            handler
            for watch, handler in server.observer._handlers.items()
            if watch.path == config.docs_dir
        )
        .copy()
        .pop()
    )
    handler.on_any_event = callback_wrapper(handler.on_any_event)


def on_page_markdown(markdown: str, page, config, files: Files) -> Optional[str]:

    if PREPROCESS_JUVIX_MD and JUVIX_AVAILABLE:
        juvix = ".juvix"
        index = "index.juvix"
        readme = "README.juvix"

        def path_change(text):
            page.file.name = page.file.name.replace(text, "")
            page.file.url = page.file.url.replace(text, "")
            page.file.dest_uri = page.file.dest_uri.replace(text, "")
            page.file.abs_dest_path = page.file.abs_dest_path.replace(text, "")

            if not page.title:
                page.title = page.file.name

        if page.file.name == index:
            path_change(index)
        elif page.file.name == readme:
            path_change(readme)
        elif page.file.name.endswith(juvix):
            path_change(juvix)
    return markdown


# AUXILIARY FUNCTIONS ----------------------------------------------------


class JuvixPreprocessor:

    def __init__(self, mkconfig: MkDocsConfig):
        self.mkconfig = mkconfig

    @property
    def site_url(self) -> str:
        _site_url = self.mkconfig.get("site_url", ROOT_URL)
        return _site_url.rstrip("/") + "/"

    @lru_cache(maxsize=128)
    @staticmethod
    def _juvix_markdown_cache_path(_filepath: Path) -> Optional[Path]:
        filepath = _filepath.absolute()
        md_filename = filepath.name.replace(".juvix.md", ".md")
        rel_to_docs = filepath.relative_to(DOCS_DIR)

        cache_filepath = MARKDOWN_JUVIX_OUTPUT.joinpath(rel_to_docs.parent).joinpath(
            md_filename
        )
        return cache_filepath

    @lru_cache(maxsize=128)
    @staticmethod
    def _juvix_markdown_cache(filepath: Path) -> Optional[str]:
        if cache_path := JuvixPreprocessor._juvix_markdown_cache_path(filepath):
            return cache_path.read_text()
        return None

    @lru_cache(maxsize=128)
    @staticmethod
    def _compute_hash_filepath_location(_filepath: Path) -> Path:
        """
        Return an absolute path for the hash file for the given file path.
        """
        hash_obj = hashlib.sha256()
        filepath = _filepath.absolute()
        hash_obj.update(filepath.as_posix().encode("utf8"))
        hash_filename = hash_obj.hexdigest()
        return HASH_DIR.joinpath(hash_filename)

    @staticmethod
    def _has_juvix_markdown_changed(filepath: Path) -> bool:
        current_hash = hash_file(filepath)
        hash_cache_path = JuvixPreprocessor._compute_hash_filepath_location(filepath)
        if hash_cache_path.exists() and (
            hash_cache_text := hash_cache_path.read_text()
        ):
            return current_hash != hash_cache_text
        return True

    def generate_markdown(self, f: Path) -> Optional[str]:
        if JuvixPreprocessor._has_juvix_markdown_changed(f):
            log.warning(
                f"Juvix file: {f} has changed, is new, or does not exist in the cache."
            )
            return self._run_juvix_markdown(f)
        return JuvixPreprocessor._juvix_markdown_cache(f)

    def _run_juvix_markdown(self, _filepath: Path) -> Optional[str]:
        """
        Runs the Juvix markdown command on the specified file path.
        This creates a new markdown file with the output of the Juvix markdown
        command. The new file is saved in the MARKDOWN_JUVIX_OUTPUT directory.
        In addition, we save the hash of the file in the HASH_DIR directory.
        """
        filepath = _filepath.absolute()
        file_path: str = filepath.as_posix()
        if file_path.endswith(".juvix.md"):
            module_name: str = os.path.basename(file_path).replace(".juvix.md", "")
            md_filename: str = module_name + ".md"
            rel_to_docs: Path = filepath.relative_to(DOCS_DIR)

            cmd: List[str] = [
                JUVIX_BIN,
                "markdown",
                "--strip-prefix=docs",
                "--folder-structure",
                f"--prefix-url={self.site_url}",
                "--stdout",
                file_path,
                "--no-colors",
            ]

            log.debug("@_run_juvix_markdown: cmd=%s", " ".join(cmd))

            completed_process = subprocess.run(cmd, cwd=DOCS_DIR, capture_output=True)

            if completed_process.returncode != 0:
                log.debug("%s", completed_process.stderr.decode("utf-8"))
                msg = completed_process.stderr.decode("utf-8")
                msg = msg.replace("\n", " ").strip()

                format_head = f"!!! failure\n\n    {msg}\n\n"

                return format_head + filepath.read_text().replace("```juvix", "```")

            md_output: str = completed_process.stdout.decode("utf-8")

            new_folder: Path = MARKDOWN_JUVIX_OUTPUT.joinpath(rel_to_docs.parent)
            new_folder.mkdir(parents=True, exist_ok=True)
            new_md_path: Path = new_folder.joinpath(md_filename)

            with open(new_md_path, "w") as f:
                f.write(md_output)

            raw_path: Path = JUVIXCODE_CACHE_DIR.joinpath(rel_to_docs)
            raw_path.parent.mkdir(parents=True, exist_ok=True)

            log.debug(
                "@_run_juvix_markdown: copying file: %s to %s", filepath, raw_path
            )
            try:
                shutil.copy(filepath, raw_path)
            except Exception as e:
                log.debug("@_run_juvix_markdown: %s", e)
            JuvixPreprocessor._write_hash_file(filepath)
            return md_output
        return None

    @staticmethod
    def _write_hash_file(filepath: Path) -> Optional[Tuple[Path, str]]:
        hash_path = JuvixPreprocessor._compute_hash_filepath_location(filepath)
        try:
            with open(hash_path, "w") as f:
                hash_filecontent = hash_file(filepath)
                f.write(hash_filecontent)
                return (hash_path, hash_filecontent)
        except Exception as e:
            log.error(f"@_write_hash_file: {e}")
            return None

    def _html_juvix_project(self, generate: bool = True) -> None:
        """Generate HTML from Juvix files."""
        log.debug(f"@_html_juvix_project: generate={generate}")
        everythingJuvix = DOCS_DIR.joinpath("everything.juvix.md")

        if not everythingJuvix.exists():
            log.warning(
                "The file 'docs/everything.juvix.md' does not exist. It is recommended to create this file to avoid excessive builds."
            )

            juvix_md_files = list(DOCS_DIR.rglob("*.juvix.md"))

            log.debug(f"@_generate_juvix_html: Found {len(juvix_md_files)} juvix files")

            for f in juvix_md_files:
                self.generate_html(f)
                if self.mkconfig and (site_dir := self.mkconfig.get("site_dir", None)):
                    _move_html_cache_to_site_dir(f, Path(site_dir))
            return

        if generate:
            log.info(
                "Generating HTML from Juvix files using 'docs/everything.juvix.md' as the main file. This may take a while the first time."
            )
            self.generate_html(everythingJuvix)
        if self.mkconfig and (site_dir := self.mkconfig.get("site_dir", None)):
            _move_html_cache_to_site_dir(everythingJuvix, Path(site_dir))
        return

    def build_aux_html(self) -> None:

        if not JUVIXCODE_CACHE_DIR.exists() or not list(JUVIXCODE_CACHE_DIR.glob("*")):
            return

        sha_filecontent = (
            JUVIXCODE_HASH_FILE.read_text() if JUVIXCODE_HASH_FILE.exists() else None
        )

        current_sha: str = compute_sha_over_folder(JUVIXCODE_CACHE_DIR)

        log.debug(f"Current sha over Juvix content: {current_sha}")
        equal_hashes = current_sha == sha_filecontent
        html_exists = HTML_CACHE_DIR.exists()

        if not equal_hashes:
            log.info("The Juvix files have changed. Regenerating the missing HTML.")
            with open(JUVIXCODE_HASH_FILE, "w") as file:
                file.write(current_sha)
            cond = not html_exists and not FAST
            self._html_juvix_project(generate=cond)
            return

        self._html_juvix_project(generate=not html_exists)

    def generate_html(self, _filepath: Path) -> None:

        filepath = _filepath.absolute()

        if HTML_CACHE_DIR.exists():
            log.debug(f"Removing folder: {HTML_CACHE_DIR}")
            shutil.rmtree(HTML_CACHE_DIR)

        HTML_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        log.debug(f"@_generate_juvix_html: html_output={HTML_CACHE_DIR}")

        rel_path = filepath.relative_to(DOCS_DIR)

        prefix_url = self.site_url + (
            (rel_path.parent.as_posix() + "/") if rel_path.parent != Path(".") else ""
        )

        log.debug(f"@_generate_juvix_html: prefix_url={prefix_url}")

        cmd = (
            [JUVIX_BIN, "html"]
            + ["--strip-prefix=docs"]
            + ["--folder-structure"]
            + [f"--output-dir={HTML_CACHE_DIR.as_posix()}"]
            + [f"--prefix-url={prefix_url}"]
            + [f"--prefix-assets={prefix_url}"]
            + [filepath.as_posix()]
        )

        log.debug(f"@_generate_juvix_html: cmd={' '.join(cmd)}")

        # FIXME: --only-src is not working in combination of the flags above
        # so, for the time being, we generate the regular html.

        log.debug(f"@_generate_juvix_html: cmd={' '.join(cmd)}")

        cd = subprocess.run(cmd, cwd=DOCS_DIR, capture_output=True)
        if cd.returncode != 0:
            log.error(cd.stderr.decode("utf-8") + "\n\n" + "Fix the error first.")
            return

        # The following is necessary as this project may
        # contain assets with changes that are not reflected
        # in the generated HTML by Juvix.
        good_assets = DOCS_DIR.joinpath("assets")
        assets_in_html = HTML_CACHE_DIR.joinpath("assets")
        if assets_in_html.exists():
            shutil.rmtree(assets_in_html, ignore_errors=True)

        shutil.copytree(
            good_assets, HTML_CACHE_DIR.joinpath("assets"), dirs_exist_ok=True
        )


def _move_html_cache_to_site_dir(filepath: Path, site_dir: Path) -> None:
    """
    Move the corresponding HTML output generated by Juvix for the given Juvix
    file to the site_dir, respecting the directory structure. It also takes into
    account that the Juvix html generation produces .html for the .juvix.md,
    which it is problematic, as it replaces the `juvix markdown` output, once
    the move to site takes place.
    """

    filepath = Path(filepath)
    if not filepath.name.endswith(".juvix.md"):
        return

    rel_path = filepath.relative_to(DOCS_DIR)

    dest_folder = site_dir.joinpath(rel_path.parent)
    dest_folder.mkdir(parents=True, exist_ok=True)

    for _file in JUVIXCODE_CACHE_DIR.rglob("*.juvix.md"):
        file = _file.absolute()
        path_rel_raw = file.relative_to(JUVIXCODE_CACHE_DIR)

        log.debug(f"move_html: file: {file}")
        if file.suffixes == [".juvix", ".md"]:
            filename = file.name

            log.debug(f"move_html: filename: {filename}")
            just_name = filename.replace(".juvix.md", "")
            html_file = just_name + ".html"
            html_file_path = HTML_CACHE_DIR / path_rel_raw.parent / html_file

            log.debug(f"move_html: html_file: {html_file_path}")
            if html_file_path.exists():
                log.debug(f"move_html: removing file {html_file_path}")
                html_file_path.unlink()

    index_file = HTML_CACHE_DIR.joinpath("index.html")
    if index_file.exists():
        index_file.unlink()

    log.debug(f"@move_html: copying folder: {HTML_CACHE_DIR} to {dest_folder}")
    shutil.copytree(HTML_CACHE_DIR, dest_folder, dirs_exist_ok=True)
    return
