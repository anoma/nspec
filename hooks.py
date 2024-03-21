"""
This module contains various hooks and functions used in the MkDocs configuration in combination with tools such as Juvix and diff
for Anoma Spec documentation.
"""

from functools import lru_cache
import logging
import os
import re
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

log: logging.Logger = logging.getLogger('mkdocs')


ROOT_DIR: Path = Path(__file__).parent.absolute()
DOCS_DIR: Path = ROOT_DIR.joinpath("docs")

DOTJUVIXMKDOCS_DIR: Path = ROOT_DIR.joinpath(".juvix-mkdocs")
DOTJUVIXMKDOCS_DIR.mkdir(parents=True, exist_ok=True)

MARKDOWN_JUVIX_OUTPUT: Path = DOTJUVIXMKDOCS_DIR.joinpath(".md")
MARKDOWN_JUVIX_OUTPUT.mkdir(parents=True, exist_ok=True)

JUVIXCODE_CACHE_DIR: Path = DOTJUVIXMKDOCS_DIR.joinpath(".juvix_md")
JUVIXCODE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
JUVIXCODE_HASH_FILE = DOTJUVIXMKDOCS_DIR.joinpath(".hash_juvix_md")

HASH_DIR: Path = DOTJUVIXMKDOCS_DIR.joinpath(".hash")
HASH_DIR.mkdir(parents=True, exist_ok=True)

HTML_CACHE_DIR: Path = DOTJUVIXMKDOCS_DIR.joinpath(".html")
HTML_CACHE_DIR.mkdir(parents=True, exist_ok=True)

DIFF_BIN: str = os.environ.get("DIFF_BIN", "diff")
DIFF_AVAILABLE = shutil.which(DIFF_BIN) is not None
DIFF_DIR = DOTJUVIXMKDOCS_DIR.joinpath(".diff")
DIFF_DIR.mkdir(parents=True, exist_ok=True)
DIFF_OPTIONS = ["--unified", "--new-file", "--text"]

VALID_FILE_PATTERN = r"(\w+)?v(\d+)((\.\w+)?\.md)"

JUVIX_BIN: str = os.environ.get("JUVIX_BIN", "juvix")
JUVIX_AVAILABLE = shutil.which(JUVIX_BIN) is not None
JUVIX_VERSION: Optional[str] = None

if JUVIX_AVAILABLE:
    cmd = [JUVIX_BIN, "--numeric-version"]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        JUVIX_VERSION = result.stdout.decode("utf-8")
        log.info(f"Running Juvix v{JUVIX_VERSION}")

# The following prevents to build html every time
# a .juvix.md file changes.
FAST = bool(int(os.environ.get("FAST", True)))

try:
    subprocess.run([JUVIX_BIN, "--version"], capture_output=True)
except FileNotFoundError:
    log.warning(
        "The Juvix binary is not available. Please install Juvix and make sure it's available in the PATH.")

try:
    subprocess.run([DIFF_BIN, "--version"], capture_output=True)
except FileNotFoundError:
    log.warning(
        "The diff binary is not available. Please install diff and make sure it's available in the PATH.")


def on_startup(command, dirty) -> None:
    """
    This is run before the build process begins. It is used to generate the
    Juvix markdown files and the corresponding HTML files. We need to isoloate
    all the .juvix.md files to compute a more effective hash. How? copy all the
    .juvix.md files to JUVIXCODE_CACHE_DIR, respecting the folder structure.
    Compute the SHA hash over the JUVIXCODE_CACHE_DIR folder and save it to
    JUVIXCODE_HASH_FILE. Generate the HTML Juvix project using the provided
    config.
    """
    timeinit = time.time()
    if not JUVIX_AVAILABLE:
        return
    
    # We need to type check first to avoid stdout messages
    # of cloning the Juvix packages in the generated markdown

    try:
        subprocess.run([JUVIX_BIN, "dependencies", "update"], capture_output=True)
    except Exception as e:
        log.error(f"@on_startup: {e}")
        return

    for _file in DOCS_DIR.rglob("*.juvix.md"):
        file: Path = _file.absolute()
        _generate_juvix_markdown(file)

    _hash: str = _compute_sha_over_folder(JUVIXCODE_CACHE_DIR)

    with open(JUVIXCODE_HASH_FILE, "w") as f:
        f.write(_hash)

    _html_juvix_project(config=None)
    endtime = time.time()
    log.info(f"Time elapsed: {endtime - timeinit:.2f} seconds")
    return


def on_files(files: Files, *, config: MkDocsConfig) -> Optional[Files]:
    for file in files:
        if ".juvix-build" in file.abs_src_path:
            files.remove(file)
    return files


def on_page_read_source(page: Page, config: MkDocsConfig) -> Optional[str]:
    filepath = Path(page.file.abs_src_path)
    if filepath.as_posix().endswith(".juvix.md") and \
            JUVIX_AVAILABLE and \
            (output := _generate_juvix_markdown(filepath)):
        return output
    return page.content


def on_post_build(config: MkDocsConfig) -> None:
    _build_aux_html(config)
    return


def on_serve(server: Any, config: MkDocsConfig, builder: Any) -> None:

    gitignore = None

    with open(ROOT_DIR / ".gitignore") as file:
        gitignore = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern, file)

    def callback_wrapper(callback: Callable[[FileSystemEvent], None]) -> Callable[[FileSystemEvent], None]:
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
                    "Hyperlinks to Juvix code external to the docs folder will not work. Only in the build mode they will generate.")
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
    juvix = ".juvix"
    index = "index.juvix"
    readme = "README.juvix"

    def path_change(text):
        page.file.name = page.file.name.replace(text, "")
        page.file.url = page.file.url.replace(text, "")
        page.file.dest_uri = page.file.dest_uri.replace(text, "")
        page.file.abs_dest_path = page.file.abs_dest_path.replace(
            text, "")

        if not page.title:
            page.title = page.file.name

    if page.file.name == index:
        path_change(index)
    elif page.file.name == readme:
        path_change(readme)
    elif page.file.name.endswith(juvix):
        path_change(juvix)

    filepath = Path(page.file.abs_src_path)

    markdown = _render_diff(markdown, filepath)
    markdown = _path_versioned_links(markdown, filepath) + markdown
    return markdown

# AUXILIARY FUNCTIONS ----------------------------------------------------


@lru_cache(maxsize=128)
def _juvix_markdown_cache_path(_filepath: Path) -> Optional[Path]:
    filepath = _filepath.absolute()
    md_filename = filepath.name.replace(".juvix.md", ".md")
    rel_to_docs = filepath.relative_to(DOCS_DIR)

    cache_filepath = MARKDOWN_JUVIX_OUTPUT \
        .joinpath(rel_to_docs.parent) \
        .joinpath(md_filename)
    return cache_filepath


@lru_cache(maxsize=128)
def _juvix_markdown_cache(filepath: Path) -> Optional[str]:
    if cache_path := _juvix_markdown_cache_path(filepath):
        return cache_path.read_text()
    return None


@lru_cache(maxsize=128)
def _compute_hash_filepath_location(_filepath: Path) -> Path:
    """
    Return an absolute path for the hash file for the given file path.
    """
    hash_obj = hashlib.sha256()
    filepath = _filepath.absolute()
    hash_obj.update(filepath.as_posix().encode("utf8"))
    hash_filename = hash_obj.hexdigest()
    return HASH_DIR.joinpath(hash_filename)


def _write_hash_file(filepath: Path) -> Optional[Tuple[Path, str]]:
    hash_path = _compute_hash_filepath_location(filepath)
    try:
        with open(hash_path, "w") as f:
            hash_filecontent = _hash_file(filepath)
            f.write(hash_filecontent)
            return (hash_path, hash_filecontent)
    except Exception as e:
        log.error(f"@_write_hash_file: {e}")
        return None


def _has_juvix_markdown_changed(filepath: Path) -> bool:
    current_hash = _hash_file(filepath)
    hash_cache_path = _compute_hash_filepath_location(filepath)
    if hash_cache_path.exists() and \
            (hash_cache_text := hash_cache_path.read_text()):
        return current_hash != hash_cache_text
    return True


def _generate_juvix_markdown(f: Path) -> Optional[str]:
    if _has_juvix_markdown_changed(f):
        log.warning(
            f"Juvix file: {f} has changed, is new, or does not exist in the cache.")
        return _run_juvix_markdown(f)
    return _juvix_markdown_cache(f)


def _run_juvix_markdown(_filepath: Path) -> Optional[str]:
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

        cmd: List[str] = [JUVIX_BIN, "markdown",
                          "--strip-prefix=docs",
                          "--folder-structure",
                          "--prefix-url=/nspec/", # FIXME once CNAME is fixed
                          "--stdout",
                          file_path,
                          "--no-colors"]

        log.debug("@_run_juvix_markdown: cmd=%s", ' '.join(cmd))

        completed_process = subprocess.run(
            cmd, cwd=DOCS_DIR, capture_output=True)

        if completed_process.returncode != 0:
            log.error("%s",
                      completed_process.stderr.decode("utf-8"))
            error_message = completed_process.stderr.decode("utf-8")
            error_message = error_message.replace("\n", " ").strip()

            format_head = f"!!! failure\n\n    {error_message}\n\n"

            return format_head + filepath.read_text()\
                .replace("```juvix", "```")

        md_output: str = completed_process.stdout.decode("utf-8")

        new_folder: Path = MARKDOWN_JUVIX_OUTPUT \
            .joinpath(rel_to_docs.parent)
        new_folder.mkdir(parents=True, exist_ok=True)
        new_md_path: Path = new_folder.joinpath(md_filename)

        with open(new_md_path, "w") as f:
            f.write(md_output)

        raw_path: Path = JUVIXCODE_CACHE_DIR.joinpath(rel_to_docs)
        raw_path.parent.mkdir(parents=True, exist_ok=True)

        log.debug("@_run_juvix_markdown: copying file: %s to %s",
                  filepath, raw_path)
        try:
            shutil.copy(filepath, raw_path)
        except Exception as e:
            log.debug("@_run_juvix_markdown: %s", e)
        _write_hash_file(filepath)
        return md_output
    return None


def _build_aux_html(config: MkDocsConfig) -> None:

    if not JUVIXCODE_CACHE_DIR.exists() or \
            not list(JUVIXCODE_CACHE_DIR.glob("*")):
        return

    sha_filecontent = JUVIXCODE_HASH_FILE\
        .read_text() if JUVIXCODE_HASH_FILE.exists() else None

    current_sha: str = _compute_sha_over_folder(JUVIXCODE_CACHE_DIR)

    log.info(f"Current sha over Juvix content: {current_sha}")
    equal_hashes = current_sha == sha_filecontent
    html_exists = HTML_CACHE_DIR.exists()

    if not equal_hashes:

        with open(JUVIXCODE_HASH_FILE, "w") as file:
            file.write(current_sha)

        cond = not html_exists and not FAST
        _html_juvix_project(config, generate=cond)
        return
    _html_juvix_project(config, generate=not html_exists)


def _path_versioned_links(markdown: str, filepath: Path) -> str:
    _prev_version = _markdown_link_filepath_version(
        filepath, -1, just_url=True)
    _next_version = _markdown_link_filepath_version(filepath, 1, just_url=True)
    if _prev_version or _next_version:
        txt = "<small class=\"version-list\">"
        if _prev_version:
            txt += f"<a class=\"version-link\" \
                href=\"{_prev_version}\">Previous version</a>"
        if _prev_version and _next_version:
            txt += " | "
        if _next_version:
            txt += f"<a class=\"version-link\" \
                    href=\"{_next_version}\">Next version</a>"
        txt += "</small>\n"
        return txt
    return ""


def _markdown_diff(diff_file: Path, indent: int = 0) -> Optional[str]:
    if not diff_file.exists():
        return None
    with open(diff_file, "r") as f:
        _diff_content = f.read()
    lines: List[str] = _diff_content.split("\n")
    lines = ["```diff"] + lines + ["```"]
    def add_indents(x): return " " * indent + x
    diff_content = "\n".join(map(add_indents, lines))
    return diff_content


def _markdown_link_filepath_version(filepath: Path, counter: int, just_url: bool = False) -> Optional[str]:
    _version = _compute_filepath_version(filepath, counter)
    if _version:
        info = _get_name_version_number(_version)
        if info:
            name, version, _ = info
            rel_path = _version.absolute().relative_to(DOCS_DIR)
            parent = rel_path.parent.as_posix()
            url = "/" + parent + "/"
            url += f"{name}v{version}.html"
            if just_url:
                return url
            return f"[{rel_path}]({url})"
    return None


def _render_diff(markdown: str, filepath, folded: bool = True) -> str:
    isMatched = _match_versioned_juvix_file(filepath)
    if not isMatched:
        return markdown
    log.debug("Matched versioned juvix file")
    diff_files = _write_diff_previous_next_version(filepath)
    if diff_files:
        prev, next = diff_files
        indent = 4 if prev else 0
        indent += 4 if next else 0
        if indent == 0:
            return markdown

        prev_diff = _markdown_diff(prev, indent) if prev else None
        next_diff = _markdown_diff(next, indent) if next else None

        callout = "???" if folded else "!!!"

        if prev_diff and next_diff:
            admonition_title = "Changes between versions"
        elif prev_diff:
            admonition_title = "Changes from previous version"
        elif next_diff:
            admonition_title = "Changes to next version"

        txt = f"{callout} diff \"{admonition_title}\"\n\n"

        md_this_version = _markdown_link_filepath_version(filepath, 0)
        md_prev_version = _markdown_link_filepath_version(filepath, -1)
        md_next_version = _markdown_link_filepath_version(filepath, 1)

        if md_this_version:
            txt += " " * 4 + f"- This file: {md_this_version}\n"
            if prev_diff and md_prev_version:
                txt += " " * 4 + f"- Previous file: {md_prev_version}\n"
            if next_diff and md_next_version:
                txt += " " * 4 + f"- Next file: {md_next_version}\n"
            txt += "\n"

        if indent == 8:
            if prev_diff:
                prev_title = "Changes from previous version"
                txt += " "*4 + f"=== \"{prev_title}:\"\n\n"
                txt += prev_diff + "\n\n"
            if next_diff:
                next_title = "Changes to next version"
                txt += " "*4 + f"=== \"{next_title}\"\n\n"
                txt += next_diff + "\n\n"
        elif indent == 4:
            txt += ((prev_diff + "\n\n") if prev_diff else "")
            txt += ((next_diff + "\n\n") if next_diff else "")
        return markdown + "\n\n" + txt

    return markdown


def _match_versioned_juvix_file(filepath: Path) -> bool:
    """
    Checks if the given file path matches the pattern for a versioned file.
    Pattern: `namevX.ext`, where `name` is the name of the file, `X` is the
    version number, and `ext` is the file extension.
    """
    filename: str = filepath.name
    match = re.match(VALID_FILE_PATTERN, filename)
    return bool(match)


def _get_name_version_number(filepath: Path) -> Optional[Tuple[str, int, str]]:
    """
    Extracts the name and version number from a file path. The filepath is
    expected to be in the format `namevX.(extension)`, where `name` is the name
    of the file and `X` is the version number.
    """
    filename: str = filepath.name
    log.debug("@_get_name_version_number: %s", filename)
    match = re.match(VALID_FILE_PATTERN, filename)
    if match:
        name: str = match.group(1) if match.group(1) else ""
        version: int = int(match.group(2))
        ext = match.group(3)
        return (name, version, ext)
    return None


def _compute_filepath_version(filepath: Path, counter: int, check_exists: bool = True) -> Optional[Path]:
    """
    Computes the new filepath with an updated version number (integer) based on the original filepath.

    Args:
        filepath (Path): The original filepath.
        counter (int): The counter to be added to the version number.

    Returns:
        Optional[Path]: The new filepath with an updated version number, or None if the version is negative.
    """
    log.debug("@_compute_filepath_version: %s", filepath)
    info = _get_name_version_number(filepath)
    if info:
        log.debug("@_compute_filepath_version: %s", info)
        name, version, _ = info
        newversion = version + counter
        if newversion <= 0:
            log.debug(
                "@_compute_filepath_version: The version number cannot be negative.")
            return None
        new_filename = f"{name}v{newversion}.juvix.md"
        log.debug("@_compute_filepath_version: new_filename=%s", new_filename)
        path = filepath.parent / new_filename
        log.debug("@_compute_filepath_version: path=%s", path)
        if check_exists and path.exists():
            log.debug("@_compute_filepath_version: path exists")
            return path
    return None


def _run_diff(_newer: Path, _older: Path) -> Optional[str]:
    """
    Run the diff command between two files or directories. If
    the files are in the same directory, the diff command is run
    with the file names. If the files are in different directories,
    the diff command is run with the absolute paths.

    Args:
        _current (Path): The path to the current file or directory.
        _other (Path): The path to the other file or directory.

    Returns:
        Optional[str]: The diff output as a string. None if the diff command fails or the files do not exist or are directories.
    """
    log.debug(f"@_run_diff: attempting to run diff between %s and %s",
              _newer, _older)

    _newer = _newer.absolute()
    _older = _older.absolute()

    if _newer.is_dir() or _older.is_dir():
        log.debug("@_run_diff: The diff command does not support directories.")
        return None

    if not _newer.exists():
        log.debug(
            "@_run_diff: The file {0} does not exist.".format(_newer.as_posix()))
        return None

    if not _older.exists():
        log.debug(
            "@_run_diff: The file {0} does not exist.".format(_older.as_posix()))
        return None

    if _newer.parent == _older.parent:
        newer_path = _newer.name
        older_path = _older.name
        folder = _newer.parent
    else:
        newer_path = _newer.as_posix()
        older_path = _older.as_posix()
        folder = None

    cmd = [DIFF_BIN] + DIFF_OPTIONS + [older_path, newer_path]
    cd = subprocess.run(cmd, cwd=folder, capture_output=True)
    log.debug("@_run_diff: %s", ' '.join(cmd))

    if cd.returncode == 0:  # the files are the same
        log.debug("@_run_diff: The diff says the files are the same.")
        return None
    if cd.returncode == 1:
        log.debug("@_run_diff: The diff command succeeded.")
        return cd.stdout.decode("utf-8")
    log.error("@_run_diff: The diff command failed.")
    log.error("@_run_diff: %s", cd.stderr.decode("utf-8"))
    return None


def _compute_diff_with_version(filepath: Path, counter: int) -> Optional[str]:
    """
    Computes the difference between the given filepath and a different version
    of the file.

    Args:
        filepath (Path): The path to the file.

        counter (int): The counter indicating the version difference.
                       A negative value indicates the previous version, while a
                       positive value indicates the next version.

    Returns:
        Optional[str]: The difference between the two versions of the file as a
        string, or None if no difference is found.
    """
    _different_version: Optional[Path] = _compute_filepath_version(
        filepath, counter)
    if _different_version:
        if counter < 0:
            return _run_diff(filepath, _different_version)
        elif counter > 0:
            return _run_diff(_different_version, filepath)
    return None


def _compute_diff_filename_version(filepath: Path, counter: int) -> Optional[str]:
    """
    Computes the filename for a diff file with a modified version number.

    Args:
        filepath (Path): The path to the original file.
        counter (int): The counter to add to the version number.

    Returns:
        Optional[str]: The computed filename for the diff file, or None if the version information is not available.
    """
    info = _get_name_version_number(filepath)
    if info:
        name, version, _ = info
        other_version = version + counter
        return f"{name}v{version}-{other_version}.diff"
    return None


def _write_diff_file_version(filepath: Path, counter: int) -> Optional[Path]:
    """
    Generate a diff file with a specific version number.

    Args:
        filepath (Path): The path to the file.
        counter (int): The version number.

    Returns:
        Optional[Path]: The path to the generated diff file, or None if no diff was generated.
    """
    log.debug(f"@_write_diff_file_version: {filepath} counter:{counter}")
    diff_output = _compute_diff_with_version(filepath, counter)
    if diff_output:
        diff_folder = DIFF_DIR / filepath.parent.relative_to(DOCS_DIR)
        diff_folder.mkdir(parents=True, exist_ok=True)
        diff_filename = _compute_diff_filename_version(filepath, counter)
        if diff_filename:
            diff_file = diff_folder / diff_filename
            with open(diff_file, "w") as f:
                f.write(diff_output)
            return diff_file
    return None


def _write_diff_previous_version(filepath: Path) -> Optional[Path]:
    return _write_diff_file_version(filepath, -1)


def _write_diff_next_version(filepath: Path) -> Optional[Path]:
    return _write_diff_file_version(filepath, 1)


def _write_diff_previous_next_version(filepath: Path) -> Optional[Tuple[Optional[Path], Optional[Path]]]:
    """
    Writes the diff between the previous and next version of a file.
    To compute the diff, the file name must match the pattern `namevX.ext`.
    """
    info = _get_name_version_number(filepath)
    if info:
        with_prev = _write_diff_previous_version(filepath)
        with_next = _write_diff_next_version(filepath)
        return (with_prev, with_next)
    log.debug(
        "@_write_diff_previous_next_version: The file name does not match the pattern `namevX.ext`.")
    log.debug(f"@_write_diff_previous_next_version: {filepath}")
    return None


def _compute_sha_over_folder(_folder_path: Path) -> str:
    """ Compute the sha with respect to the structure of a folder. """

    folder_path = _folder_path.absolute().as_posix()
    sha_hash: hashlib._Hash = hashlib.sha256()
    for root, dirs, files in os.walk(folder_path):
        for names in sorted(dirs):
            sha_hash.update(names.encode('utf-8'))
        for filename in sorted(files):
            file_path = os.path.join(root, filename)
            sha_hash.update(file_path.encode('utf-8'))
            _hash_file_hash_obj(sha_hash, Path(file_path))
    return sha_hash.hexdigest()


def _hash_file_hash_obj(hash_obj, filepath: Path):
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hash_obj.update(chunk)


def _hash_file(_filepath: Path):
    filepath = _filepath.absolute()
    _hash_obj = hashlib.sha256()
    _hash_file_hash_obj(_hash_obj, filepath)
    return _hash_obj.hexdigest()


def _generate_juvix_html(_filepath: Path) -> None:

    filepath = _filepath.absolute()

    if HTML_CACHE_DIR.exists():
        log.debug(f"Removing folder: {HTML_CACHE_DIR}")
        shutil.rmtree(HTML_CACHE_DIR)

    HTML_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    log.debug(f"@_generate_juvix_html: html_output={HTML_CACHE_DIR}")

    rel_path = filepath.relative_to(DOCS_DIR)
    prefix_url = "/nspec/" + ((rel_path.parent.as_posix() + "/")
                        if rel_path.parent != Path(".") else "")

    cmd = [JUVIX_BIN, "html"] + \
        ["--strip-prefix=docs"] + \
        ["--folder-structure"] + \
        [f"--output-dir={HTML_CACHE_DIR.as_posix()}"] + \
        [f"--prefix-url={prefix_url}"] + \
        [f"--prefix-assets=/nspec/"] + \
        [filepath.as_posix()]

    # FIXME: --only-src is not working in combination of the flags above
    # so, for the time being, we generate the regular html.

    log.debug(f"@_generate_juvix_html: cmd={' '.join(cmd)}")

    cd = subprocess.run(cmd, cwd=DOCS_DIR, capture_output=True)
    if cd.returncode != 0:
        log.error(cd.stderr.decode("utf-8") + "\n\n"
                  + "Fix the error first.")
        return

    # The following is necessary as this project may
    # contain assets with changes that are not reflected
    # in the generated HTML by Juvix.
    good_assets = DOCS_DIR.joinpath("assets")
    assets_in_html = HTML_CACHE_DIR.joinpath("assets")
    if assets_in_html.exists():
        shutil.rmtree(assets_in_html, ignore_errors=True)

    shutil.copytree(good_assets, HTML_CACHE_DIR.joinpath("assets"),
                    dirs_exist_ok=True)


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

        log.debug(f"@_generate_juvix_html: file: {file}")
        if file.suffixes == [".juvix", ".md"]:
            filename = file.name

            log.debug(f"@_generate_juvix_html: filename: {filename}")
            just_name = filename.replace(".juvix.md", "")
            html_file = just_name + ".html"
            html_file_path = HTML_CACHE_DIR \
                .joinpath(path_rel_raw.parent) \
                .joinpath(html_file)

            log.debug(f"@_generate_juvix_html: html_file: {html_file_path}")
            if html_file_path.exists():
                log.debug(
                    f"@_generate_juvix_html: removing file {html_file_path}")
                html_file_path.unlink()

    index_file = HTML_CACHE_DIR.joinpath("index.html")
    if index_file.exists():
        index_file.unlink()

    log.debug(
        f"@generate_juvix_html: copying folder: {HTML_CACHE_DIR} to {dest_folder}")
    shutil.copytree(HTML_CACHE_DIR, dest_folder, dirs_exist_ok=True)
    return


def _html_juvix_project(config: Optional[MkDocsConfig],
                        generate: bool = True
                        ) -> None:
    """ Generate HTML from Juvix files. """

    everythingJuvix = DOCS_DIR.joinpath("everything.juvix.md")

    if not everythingJuvix.exists():
        log.warning(
            "The file 'docs/everything.juvix.md' does not exist. It is recommended to create this file to avoid excessive builds.")

        juvix_md_files = list(DOCS_DIR.rglob("*.juvix.md"))

        log.debug(
            f"@_generate_juvix_html: Found {len(juvix_md_files)} juvix files")

        for f in juvix_md_files:
            _generate_juvix_html(f)
            if config and (site_dir := config.get("site_dir", None)):
                _move_html_cache_to_site_dir(f, Path(site_dir))
        return

    if generate:
        log.info(
            "Generating HTML from Juvix files using 'docs/everything.juvix.md' as the main file. This may take a while the first time.")
        _generate_juvix_html(everythingJuvix)
    if config and (site_dir := config.get("site_dir", None)):
        _move_html_cache_to_site_dir(everythingJuvix, Path(site_dir))
    return
