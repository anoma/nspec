"""
This hooks module provides a way to render diffs between files under the same
file name but with different version numbers in the same folder. The valid file
name pattern is `namevX.ext`, where `name` is the name of the file, `X` is the
version number, and `ext` is the file extension.
"""

import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urljoin

from common.utils import fix_site_url
from mkdocs.structure.files import Files

log: logging.Logger = logging.getLogger("mkdocs")

ROOT_DIR: Path = Path(__file__).parent.parent.absolute()
DOCS_DIR: Path = ROOT_DIR.joinpath("docs")

CACHE_HOOKS: Path = ROOT_DIR.joinpath(".hooks")
CACHE_HOOKS.mkdir(parents=True, exist_ok=True)

VERSIONED_FILE_PATTERN = r"(.+)?v(\d+)((\.\w+)?\.md)"

DIFF_ENABLED: bool = bool(os.environ.get("DIFF_ENABLED", True))

if DIFF_ENABLED:
    log.info("Diff hooks enabled.")

    DIFF_BIN: str = os.environ.get("DIFF_BIN", "diff")
    DIFF_AVAILABLE = shutil.which(DIFF_BIN) is not None

    DIFF_DIR = CACHE_HOOKS.joinpath(".diff")
    DIFF_DIR.mkdir(parents=True, exist_ok=True)
    DIFF_OPTIONS = ["--unified", "--new-file", "--text"]

    try:
        subprocess.run([DIFF_BIN, "--version"], capture_output=True)
    except FileNotFoundError:
        log.warning(
            "The diff binary is not available. Please install diff and make sure it's available in the PATH."
        )

    def on_config(config, **kwargs):
        return fix_site_url(config)

    class DiffPreprocessor:
        def __init__(self, config):
            self.mkconfig = config
            self.site_url = config.get("site_url", "")

        def _path_versioned_links(self, markdown: str, filepath: Path) -> str:
            _prev_version = self._markdown_link_filepath_version(
                filepath, -1, just_url=True
            )
            _next_version = self._markdown_link_filepath_version(
                filepath, 1, just_url=True
            )
            if _prev_version or _next_version:
                txt = '<small class="version-list">'
                if _prev_version:
                    txt += f'<a class="version-link" \
                        href="{_prev_version}">Previous version</a>'
                if _prev_version and _next_version:
                    txt += " | "
                if _next_version:
                    txt += f'<a class="version-link" \
                            href="{_next_version}">Next version</a>'
                txt += "</small>\n"
                return txt
            return ""

        def _markdown_diff(self, diff_file: Path, indent: int = 0) -> Optional[str]:
            if not diff_file.exists():
                return None

            with open(diff_file, "r") as f:
                _diff_content = f.read()

            lines: List[str] = _diff_content.split("\n")
            lines = ["```diff"] + lines + ["```"]

            def add_indents(x):
                return " " * indent + x

            diff_content = "\n".join(map(add_indents, lines))
            return diff_content

        def _markdown_link_filepath_version(
            self, filepath: Path, counter: int, just_url: bool = False
        ) -> Optional[str]:
            _version = self._compute_filepath_version(filepath, counter)
            if _version:
                info = self._get_name_version_number(_version)
                if info:
                    name, version, _ = info
                    rel_path = (
                        _version.absolute()
                        .relative_to(DOCS_DIR)
                        .as_posix()
                        .replace(".juvix", "")
                        .replace(".md", ".html")
                    )

                    url = urljoin(self.site_url, rel_path)

                    if just_url:
                        return url
                    return f"[{rel_path}]({url})"
            return None

        def _render_diff(
            self, markdown: str, filepath: Path, folded: bool = True
        ) -> str:
            isMatched = self._match_versioned_file(filepath)

            log.debug(f"filepath: {filepath}")
            log.debug(f"isMatched: {isMatched}")

            if not isMatched:
                return markdown
            log.debug("Matched versioned file")
            diff_files = self._write_diff_previous_next_version(filepath)
            log.debug(f"diff_files: {diff_files}")
            if diff_files:
                prev, next = diff_files
                indent = 4 if prev else 0
                indent += 4 if next else 0
                if indent == 0:
                    return markdown

                prev_diff = self._markdown_diff(prev, indent) if prev else None
                next_diff = self._markdown_diff(next, indent) if next else None

                callout = "???" if folded else "!!!"

                if prev_diff and next_diff:
                    admonition_title = "Changes between versions"
                elif prev_diff:
                    admonition_title = "Changes from previous version"
                elif next_diff:
                    admonition_title = "Changes to next version"

                txt = f'{callout} diff "{admonition_title}"\n\n'

                md_this_version = self._markdown_link_filepath_version(filepath, 0)
                md_prev_version = self._markdown_link_filepath_version(filepath, -1)
                md_next_version = self._markdown_link_filepath_version(filepath, 1)

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
                        txt += " " * 4 + f'=== "{prev_title}:"\n\n'
                        txt += prev_diff + "\n\n"
                    if next_diff:
                        next_title = "Changes to next version"
                        txt += " " * 4 + f'=== "{next_title}"\n\n'
                        txt += next_diff + "\n\n"
                elif indent == 4:
                    txt += (prev_diff + "\n\n") if prev_diff else ""
                    txt += (next_diff + "\n\n") if next_diff else ""
                return markdown + "\n\n" + txt

            return markdown

        def _match_versioned_file(self, filepath: Path) -> bool:
            """
            Checks if the given file path matches the pattern for a versioned file.
            Pattern: `namevX.ext`, where `name` is the name of the file, `X` is the
            version number, and `ext` is the file extension.
            """
            filename: str = filepath.name
            match = re.match(VERSIONED_FILE_PATTERN, filename)
            return bool(match)

        def _get_name_version_number(
            self, filepath: Path
        ) -> Optional[Tuple[str, int, str]]:
            """
            Extracts the name and version number from a file path. The filepath is
            expected to be in the format `namevX.(extension)`, where `name` is the name
            of the file and `X` is the version number.
            """
            filename: str = filepath.name
            log.debug("@_get_name_version_number: %s", filename)
            match = re.match(VERSIONED_FILE_PATTERN, filename)
            if match:
                name: str = match.group(1) if match.group(1) else ""
                version: int = int(match.group(2))
                ext = match.group(3)
                return (name, version, ext)
            return None

        def _compute_filepath_version(
            self, filepath: Path, counter: int, check_exists: bool = True
        ) -> Optional[Path]:
            """
            Computes the new filepath with an updated version number (integer) based on the original filepath.

            Args:
                filepath (Path): The original filepath.
                counter (int): The counter to be added to the version number.

            Returns:
                Optional[Path]: The new filepath with an updated version number, or None if the version is negative.
            """
            log.debug("@_compute_filepath_version: %s", filepath)
            info = self._get_name_version_number(filepath)
            if info:
                log.debug("@_compute_filepath_version: %s", info)
                name, version, ext = info
                newversion = version + counter
                if newversion <= 0:
                    log.debug(
                        "@_compute_filepath_version: The version number cannot be negative."
                    )
                    return None
                new_filename = f"{name}v{newversion}{ext}"
                log.debug("@_compute_filepath_version: new_filename=%s", new_filename)
                path = filepath.parent / new_filename
                log.debug("@_compute_filepath_version: path=%s", path)
                if check_exists and path.exists():
                    log.debug("@_compute_filepath_version: path exists")
                    return path
            return None

        def _run_diff(self, _newer: Path, _older: Path) -> Optional[str]:
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
            log.debug(f"Attempting to run diff between {_newer} and {_older}")

            _newer = _newer.absolute()
            _older = _older.absolute()

            if _newer.is_dir() or _older.is_dir():
                log.debug("The diff command does not support directories.")
                return None

            if not _newer.exists():
                log.debug(f"The file {_newer.as_posix()} does not exist.")
                return None

            if not _older.exists():
                log.debug(f"The file {_older.as_posix()} does not exist.")
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
            log.debug("%s", " ".join(cmd))

            if cd.returncode == 0:
                log.debug("The diff says that the files are the same.")
                return None
            if cd.returncode == 1:
                log.debug("The diff command succeeded.")
                return cd.stdout.decode("utf-8")
            log.error(f"The diff command failed:\n{cd.stderr.decode('utf-8')}")
            return None

        def _compute_diff_with_version(
            self, filepath: Path, counter: int
        ) -> Optional[str]:
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
            _different_version: Optional[Path] = self._compute_filepath_version(
                filepath, counter
            )
            if _different_version:
                if counter < 0:
                    return self._run_diff(filepath, _different_version)
                elif counter > 0:
                    return self._run_diff(_different_version, filepath)
            return None

        def _compute_diff_filename_version(
            self, filepath: Path, counter: int
        ) -> Optional[str]:
            """
            Computes the filename for a diff file with a modified version number.

            Args:
                filepath (Path): The path to the original file.
                counter (int): The counter to add to the version number.

            Returns:
                Optional[str]: The computed filename for the diff file, or None if the version information is not available.
            """
            info = self._get_name_version_number(filepath)
            if info:
                name, version, _ = info
                other_version = version + counter
                return f"{name}v{version}-{other_version}.diff"
            return None

        def _write_diff_file_version(
            self, filepath: Path, counter: int
        ) -> Optional[Path]:
            """
            Generate a diff file with a specific version number.

            Args:
                filepath (Path): The path to the file.
                counter (int): The version number.

            Returns:
                Optional[Path]: The path to the generated diff file, or None if no diff was generated.
            """
            log.debug(f"Filepath: {filepath} counter:{counter}")
            diff_output = self._compute_diff_with_version(filepath, counter)
            if diff_output:
                diff_folder = DIFF_DIR / filepath.parent.relative_to(DOCS_DIR)
                diff_folder.mkdir(parents=True, exist_ok=True)
                diff_filename = self._compute_diff_filename_version(filepath, counter)
                if diff_filename:
                    diff_file = diff_folder / diff_filename
                    with open(diff_file, "w") as f:
                        f.write(diff_output)
                    return diff_file
            return None

        def _write_diff_previous_version(self, filepath: Path) -> Optional[Path]:
            return self._write_diff_file_version(filepath, -1)

        def _write_diff_next_version(self, filepath: Path) -> Optional[Path]:
            return self._write_diff_file_version(filepath, 1)

        def _write_diff_previous_next_version(
            self,
            filepath: Path,
        ) -> Optional[Tuple[Optional[Path], Optional[Path]]]:
            """
            Writes the diff between the previous and next version of a file.
            To compute the diff, the file name must match the pattern `namevX.ext`.
            """
            info = self._get_name_version_number(filepath)
            if info:
                with_prev = self._write_diff_previous_version(filepath)
                with_next = self._write_diff_next_version(filepath)
                return (with_prev, with_next)
            log.debug(
                f"The file name ({filepath}) does not match the pattern `namevX.ext`."
            )
            return None

        def add_diff_markdown(self, markdown: str, filepath: Path) -> str:
            _markdown = self._render_diff(markdown, filepath)
            markdown = self._path_versioned_links(_markdown, filepath) + _markdown
            return markdown

    def on_page_markdown(markdown: str, page, config, files: Files) -> Optional[str]:
        filepath = Path(page.file.abs_src_path)
        if not DIFF_AVAILABLE:
            return markdown
        differ = DiffPreprocessor(config)
        return differ.add_diff_markdown(markdown, filepath)
