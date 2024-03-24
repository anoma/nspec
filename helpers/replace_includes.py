import os
import re
from pathlib import *


def replace_includes(line):
    include_re = r'{{\s*#include ([^}]+)}}'
    return re.sub(include_re, r'--8<-- "\1"', line)

def replace_patterns_anchors(line):
    """
    Replace anchor patterns in a given line of an SML, SIG, or FUN file.
    """
    line = re.sub(r'([^\s]+) ANCHOR: ([^\s]+) ([^\s]+)', r'\1 --8<-- [start:\2] \3', line)
    line = re.sub(r'([^\s]+) ANCHOR_END: ([^\s]+) ([^\s]+)',
                  r'\1 --8<-- [end:\2] \3', line)
    return line


def process_file(file_path):
    """
    Process a single file, replacing patterns as required based on file type.
    """
    if ".git" in file_path or ".cache" in file_path:
        return
    _, file_extension = os.path.splitext(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    if file_extension in ['.md','.sml', '.sig', '.fun']:
        for line in lines:
            line = replace_patterns_anchors(line)
            line = replace_includes(line)
            new_lines.append(line)
    else:
        new_lines = lines

    # Write the changes back to the file if there are modifications
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


def process_directory(directory: Path):
    try:
        directory = directory.resolve().absolute()
    except FileNotFoundError:
        raise ValueError(f"{directory} does not exist")
    if not directory.is_dir():
        raise ValueError(f"{directory} is not a directory")
    for root, _, files in os.walk(directory):
        print(f"Processing directory {root}")
        for file in files:
            if file.endswith(('.md', '.sml', '.sig', '.fun')):
                print(f"\tProcessing {file}...")
                file_path = os.path.join(root, file)
                process_file(file_path)


if __name__ == "__main__":
    # directory is one level up from the script joined with the 'docs' directory
    directory = Path(__file__).parent.parent
    process_directory(directory)
    print("Processing complete.")
