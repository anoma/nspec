import os
import re
from pathlib import *


def replace_patterns_md(line, in_sml_block):
    """
    Replace patterns in a given line based on whether it is inside an SML code block.
    """
    include_re = r'{{#include ((../)+SML/([^}]+))}}'
    if in_sml_block:
        # Pattern inside SML code blocks
        return re.sub(include_re,
                      r'--8<-- "./formal/SML/\3"', line)
    else:
        # Pattern outside SML code blocks
        return re.sub(include_re, r'--8<-- "./formal/SML/\3"\n', line)


def replace_patterns_sml(line):
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
    _, file_extension = os.path.splitext(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    if file_extension == '.md':
        in_sml_block = False
        for line in lines:
            # Check for SML code block start or end
            if line.strip() == "```sml":
                in_sml_block = not in_sml_block
                new_lines.append(line)
            else:
                new_lines.append(replace_patterns_md(line, in_sml_block))
    elif file_extension in ['.sml', '.sig', '.fun']:
        for line in lines:
            new_lines.append(replace_patterns_sml(line))

    # Write the changes back to the file if there are modifications
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


def process_directory(directory: Path):
    # resolve the directory path
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
                print(f"Processing {file}...")
                file_path = os.path.join(root, file)
                process_file(file_path)


if __name__ == "__main__":
    # directory is one level up from the script joined with the 'docs' directory
    directory = Path(__file__).parent.parent
    print(f"Processing files in {directory} ..")
    process_directory(directory)
    print("Processing complete.")
