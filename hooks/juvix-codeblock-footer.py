import logging
import subprocess
from pathlib import Path
from typing import Optional
from mkdocs.config.defaults import MkDocsConfig
from common.utils import fix_site_url

log: logging.Logger = logging.getLogger("mkdocs")

ROOT_DIR = Path(__file__).parent.parent.absolute()
DOCS_DIR = ROOT_DIR / "docs"
ASSET_PATH = Path("assets") / "css" / "juvix-codeblock-footer.css"
CSS_PATH = DOCS_DIR / ASSET_PATH


def get_juvix_version() -> Optional[str]:
    """Get Juvix compiler version."""
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


def generate_css_file() -> Optional[Path]:
    """Generate the CSS file with the Juvix version in the content if it doesn't already exist or content has changed."""
    version = get_juvix_version()
    if version is None:
        log.error("Cannot generate CSS file without Juvix version.")
        return None

    css_content = f"""
code.juvix::after {{
    font-family: var(--md-code-font-family);
    content: "Powered by Juvix v{version}";
    font-size: 10px;
    color: var(--md-juvix-codeblock-footer);
    float: right;
}}
"""

    CSS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSS_PATH.open("w") as f:
        f.write(css_content)

    log.info("CSS file generated at %s.", CSS_PATH)
    return CSS_PATH


def on_pre_build(config: MkDocsConfig) -> None:
    generate_css_file()


def on_config(config: MkDocsConfig) -> MkDocsConfig:
    config = fix_site_url(config)
    config["extra_css"].append(ASSET_PATH.as_posix())
    return config
