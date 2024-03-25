import os
import re
from pathlib import *


# def replace_includes(line):
#     include_re = r'{{\s*#include ([^}]+)}}'
#     return re.sub(include_re, r'--8<-- "\1"', line)

# def replace_md_supperfences(line):
#     if ".md" in line:
#         include_re = r'(\s*)--8<-- (.+)'
#         if re.match(include_re, line):
#             print(line)
#             return f"```markdown\n{line}```\n"
#     return line

def add_markdown_div_class(line):
    """
    Add a class to a markdown div.
    """
    line = re.sub(r'<div\s+class=(.+) [^markdown]>', r'<div class=\1 markdown>\n', line)
    return line

def replace_patterns_anchors(line):
    """
    Replace anchor patterns:
    If we see "%% ANCHOR: <name> <id>", we replace it with 
    "--8<-- [start:<name>] <id>"
    If we see "%% ANCHOR_END: <name> <id>", we replace it with
    "--8<-- [end:<name>] <id>"
    """
    # Corrected regular expressions to capture 'name' and 'id'
    anchor_re = r'\%\% ANCHOR: (.+)'
    anchor_end_re = r'\%\% ANCHOR_END: (.+)'
    print_line = False
    if "%% ANCHOR" in line:
        print("****")
        print(line)
        print("====")
        print_line = True
    # Using `re.search` instead of `re.match` because `re.match` only matches at the beginning of the string.
    if re.search(anchor_re, line):
        line = re.sub(anchor_re, r'%% --8<-- [start:\1]', line)
    elif re.search(anchor_end_re, line):
        line = re.sub(anchor_end_re, r'%% --8<-- [end:\1]', line)
    if print_line:
        print("Original line:")
        print(line)
        print("-------")
    return line



def process_file(file_path, directory=None):
    """
    Process a single file, replacing patterns as required based on file type.
    """

    if ".juvix" in file_path or "env/lib" in file_path:
        return

    if ".git" in file_path or ".cache" in file_path:
        return
    _, file_extension = os.path.splitext(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    relative_path_to_root = os.path.relpath(file_path, start=directory)
    # print(f"{relative_path_to_root}")

    new_lines = []
    if file_extension in ['.md','.sml', '.sig', '.fun']:
        i = 0
        while i < len(lines):
            line = lines[i]
            line = add_markdown_div_class(line)
            _line = replace_patterns_anchors(line)
            if line != _line:
                print(f"Replacing {line} with {_line}")
                line = _line
            new_lines.append(line)
            i += 1
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
        for file in files:
            if file.endswith(('.md', '.sml', '.sig', '.fun')):
                file_path = os.path.join(root, file)
                process_file(file_path, directory)


if __name__ == "__main__":
    # directory is one level up from the script joined with the 'docs' directory
    directory = Path(__file__).parent.parent
    process_directory(directory)
