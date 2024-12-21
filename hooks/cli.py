import re
from pathlib import Path

import click
import questionary
from colorama import Fore  # type: ignore

ROOT_PATH = Path("./").resolve()
DOCS_PATH = ROOT_PATH / "docs"
TEMPLATE_MIN_PATH = DOCS_PATH / "tutorial" / "engines"
ARCH_NODE_PATH = DOCS_PATH / "arch" / "node"
ENGINE_PATH = ARCH_NODE_PATH / "engines"


def transform_file(
    input_path: Path, output_path: Path, replacements: list[tuple[str, str]]
):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        content = input_path.read_text()
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        output_path.write_text(content)
        click.echo(
            f"Created {Fore.GREEN}{output_path.relative_to(ENGINE_PATH)}{Fore.RESET} from {Fore.GREEN}{input_path.relative_to(TEMPLATE_MIN_PATH)}{Fore.RESET}"
        )
    except FileNotFoundError:
        click.echo(f"Error: Could not find file {input_path}", err=True)
    except Exception as e:
        click.echo(f"Error processing {input_path}: {str(e)}", err=True)


# -- CLI --
@click.group()
def cli():
    """Command line tool to assist with the Anoma specification writing process"""
    pass


@cli.group()
def new():
    """Create new stuff"""
    pass


@new.command()
@click.argument("name", type=click.STRING, required=False)
def engine(name):
    """Create a new engine from template"""
    while not name:
        name = questionary.text(
            "What is the name of the new engine? (CamelCase is recommended, e.g: `Indexer`)"
        ).ask()

    # use snake case
    snake_name = (
        name.lower().replace(" ", "_").replace("-", "_").replace(".", "_").strip()
    )
    click.echo(f"Creating engine {Fore.GREEN}{name}{Fore.RESET}")

    template_minimum_prefix = "template_minimum"
    base_files = ["", "_messages", "_config", "_environment", "_behaviour"]

    for base_name in base_files:
        input_path = (
            TEMPLATE_MIN_PATH / f"{template_minimum_prefix}{base_name}.juvix.md"
        )
        output_path = ENGINE_PATH / f"{snake_name}{base_name}.juvix.md"
        replacements = [
            (r"tutorial\.engines", "arch.node.engines"),
            (r"template([_-])minimum", snake_name),
            (r"Template( )?Minimum", name),
        ]
        transform_file(input_path, output_path, replacements)

    # add the engine to the engines list in docs/everything.juvix.md
    everything_path = DOCS_PATH / "everything.juvix.md"
    everything_content = everything_path.read_text()
    if f"import arch.node.engines.{snake_name}_messages;" not in everything_content:
        more_start = "-- Add more engines here"
        more_start_index = everything_content.find(more_start) + len(more_start)
        everything_content = (
            everything_content[:more_start_index]
            + "\n\n"
            + f"import arch.node.engines.{snake_name}_messages;\n"
            + f"import arch.node.engines.{snake_name}_config;\n"
            + f"import arch.node.engines.{snake_name}_environment;\n"
            + f"import arch.node.engines.{snake_name}_behaviour;\n"
            + f"import arch.node.engines.{snake_name};\n"
            + everything_content[more_start_index:]
        )
        everything_path.write_text(everything_content)

    def add_import(content: str, import_name: str):
        if f"import arch.node.engines.{import_name} open;" not in content:
            import_start = "-- Add imports here"
            import_end = content.find(import_start) + len(import_start)
            content = (
                content[:import_end]
                + f"\n    import arch.node.engines.{import_name} open;\n"
                + content[import_end:]
            )
        return content

    def update_anoma_registry(
        file_suffix, type_prefix, type_suffix, import_suffix, more_marker
    ):
        file_path = ARCH_NODE_PATH / "types" / f"anoma_{file_suffix}.juvix.md"
        file_content = file_path.read_text()
        if (
            f"import arch.node.engines.{snake_name}_{import_suffix};"
            not in file_content
        ):
            file_content = add_import(file_content, snake_name + f"_{import_suffix}")
            if more_marker in file_content:
                more_start_index = file_content.find(more_marker) + len(more_marker)
                new_line = f"  | {type_prefix}{name} {name}{type_suffix}\n"
                if new_line.strip() not in file_content[more_start_index:]:
                    file_content = (
                        file_content[:more_start_index]
                        + "\n\n"
                        + new_line
                        + file_content[more_start_index:]
                    )
            file_path.write_text(file_content)

    update_anoma_registry(
        "message", "Msg", "Msg", "messages", "-- Add more messages here"
    )
    update_anoma_registry(
        "config", "Cfg", "Cfg", "config", "-- Add more configurations here"
    )
    update_anoma_registry(
        "environment", "Env", "Env", "environment", "-- Add more environments here"
    )

    click.echo(f"Engine {Fore.GREEN}{name}{Fore.RESET} created successfully")
    click.echo(
        "Don't forget to:\n"
        "- update `mkdocs.yml` to add the new engine to the navigation menu\n"
        f"- review `docs/arch/node/types/anoma_config.juvix.md`, specially where we put new stuff for {name}\n"
        f"- review `docs/arch/node/types/anoma_message.juvix.md`, specially where we put new stuff for {name}\n"
        f"- review `docs/arch/node/types/anoma_environment.juvix.md`, specially where we put new stuff for {name}\n"
    )


if __name__ == "__main__":
    cli()
