"""
This module provides a CLI tool to assist with the Anoma specification writing process.
"""
import re
from pathlib import Path

import click
from colorama import Fore  # type: ignore

ROOT_PATH = Path("./").resolve()
DOCS_PATH = ROOT_PATH / "docs"


# -- CLI --
@click.group()
def cli():
    """Command line tool to assist with the Anoma specification writing process"""
    pass

@cli.command()
def bump():
    """Bump the version of the specification"""
    version = questionary.text(
        "What is the version of the new version? (e.g: `1.0.0`)"
    ).ask()
    click.echo(f"Creating version {Fore.GREEN}{version}{Fore.RESET}")
    confirm = questionary.confirm(
        "Are you sure you want to create this version? (y/n)"
    ).ask()
    if not confirm:
        click.echo("Aborting")
        return

    # Update the version in the mkdocs.yml file
    mkdocs_path = ROOT_PATH / "mkdocs.yml"
    mkdocs_content = mkdocs_path.read_text()
    mkdocs_content = re.sub(r"v[0-9]+\.[0-9]+\.[0-9]+", f"v{version}", mkdocs_content)
    mkdocs_path.write_text(mkdocs_content)

    # update the version in pyproject.toml
    pyproject_path = ROOT_PATH / "pyproject.toml"
    pyproject_content = pyproject_path.read_text()
    pyproject_content = re.sub(
        r"version = \"[0-9]+\.[0-9]+\.[0-9]+\"",
        f'version = "{version}"',
        pyproject_content,
    )
    pyproject_path.write_text(pyproject_content)

    # update the version in docs/Package.juvix
    package_path = DOCS_PATH / "Package.juvix"
    package_content = package_path.read_text()
    #  mkVersion X Y Z;
    version_parts = version.split(".")
    package_content = re.sub(
        r"mkVersion [0-9]+ [0-9]+ [0-9]+;",
        f"mkVersion {version_parts[0]} {version_parts[1]} {version_parts[2]};",
        package_content,
    )
    package_path.write_text(package_content)


if __name__ == "__main__":
    cli()
