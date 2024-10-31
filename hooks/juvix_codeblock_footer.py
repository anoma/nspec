import logging
import subprocess
from pathlib import Path
from typing import Optional

from common.utils import fix_site_url
from mkdocs.config.defaults import MkDocsConfig

log: logging.Logger = logging.getLogger("mkdocs")

ROOT_DIR = Path(__file__).parent.parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"
ASSET_PATH = Path("assets") / "css"

JUVIX_FOOTER_CSS_FILE = DOCS_DIR / ASSET_PATH / "juvix_codeblock_footer.css"
JUVIX_FOOTER_CSS_FILE.parent.mkdir(parents=True, exist_ok=True)

CACHE_DIR: Path = ROOT_DIR.joinpath(".hooks")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_JUVIX_VERSION_FILE = CACHE_DIR / ".juvix-version"


def get_juvix_version() -> Optional[str]:
    try:
        result = subprocess.run(
            ["juvix", "--numeric-version"],
            stdout=subprocess.PIPE,
            check=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log.error("Failed to get Juvix version: %s", e)
        return None


def generate_css_file(version: Optional[str] = None) -> Optional[Path]:
    JUVIX_FOOTER_CSS_FILE.parent.mkdir(parents=True, exist_ok=True)
    JUVIX_FOOTER_CSS_FILE.write_text(
        f"""
code.juvix::after {{
    font-family: var(--md-code-font-family);
    content: "Juvix v{version}";
    font-size: 10px;
    color: var(--md-juvix-codeblock-footer);
    float: right;
}}
"""
    )
    log.info("CSS file generated at %s.", JUVIX_FOOTER_CSS_FILE)
    return JUVIX_FOOTER_CSS_FILE


def on_pre_build(config: MkDocsConfig) -> None:
    version = get_juvix_version()
    if version is None:
        log.error(
            "Cannot generate CSS file without Juvix version. Make sure Juvix is installed."
        )
        return

    need_to_write = (
        not CACHE_JUVIX_VERSION_FILE.exists() or not JUVIX_FOOTER_CSS_FILE.exists()
    )
    read_version = (
        CACHE_JUVIX_VERSION_FILE.read_text().strip() if not need_to_write else None
    )
    if read_version != version:
        CACHE_JUVIX_VERSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        CACHE_JUVIX_VERSION_FILE.write_text(version)
        need_to_write = True
    if need_to_write:
        generate_css_file(version)
    return None


def on_config(config: MkDocsConfig) -> MkDocsConfig:
    config = fix_site_url(config)
    config["extra_css"].append(ASSET_PATH.as_posix())
    return config
