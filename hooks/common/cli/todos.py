"""
This script reports all the todo entries in the markdown files in the given
directory. You could use grep but this script is more user-friendly and provides
a better output.
"""

import glob
import os
import sys

import click


def find_todos(file_path):
    """
    Reports the todo entries in a given file.
    """
    num_todo_entries = 0
    abs_path = os.path.abspath(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i, line in enumerate(lines, start=1):

            if line.strip().startswith("!!! todo"):
                num_todo_entries += 1
                _line = line.lstrip()
                nwspaces = len(line) - len(_line)

                message = ""
                for j in range(i + 1, len(lines)):
                    if len(lines[j].strip()) == 0:
                        continue
                    if lines[j].startswith(" " * nwspaces):
                        message += lines[j].strip()
                    else:
                        break
                short_message = message[:200] + (message[200:] and "...")

                # print the abs_path in red color
                print(
                    f"\033[91m{abs_path}\033[0m:{i}:1:\n  {short_message.strip()}\n",
                    file=sys.stderr,
                )

    return num_todo_entries


def find_all_todos(directory_path):
    total = 0
    for markdown_file in glob.glob(
        os.path.join(directory_path, "**", "*.md"), recursive=True
    ):
        total += find_todos(markdown_file)

    print(f"Todo entries: {total}")


@click.command()
@click.argument(
    "folder", default="./docs", type=click.Path(exists=True, file_okay=False)
)
def main(folder):
    """
    Reports all the todo entries in the markdown files in the given directory.
    """
    find_all_todos(folder)


if __name__ == "__main__":
    main()
