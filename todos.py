"""
This script reports all the todo entries in the markdown files in the given directory.
"""
import os
import glob
import sys

def find_todos(file_path):
    """
    Reports the todo entries in a given file.
    """
    num_todo_entries = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i, line in enumerate(lines, start=1):
            if line.strip().startswith("!!! todo"):
                num_todo_entries += 1
                _line = line.lstrip()
                nwspaces = len(line) - len(_line)

                message = ""
                for j in range(i+1, len(lines)):
                    if len(lines[j].strip()) == 0:
                        continue
                    if lines[j].startswith(' '* nwspaces):
                        message += lines[j].strip()
                    else:
                        break  
                short_message = message[:50] + (message[50:] and '...')       

                abs_path = os.path.abspath(file_path)

                print(f"{abs_path}:{i}:1:\n  {short_message.strip()}\n", file=sys.stderr)
    return num_todo_entries                


def find_all_todos(directory_path):
    total = 0
    for markdown_file in glob.glob(os.path.join(directory_path, '**', '*.md'), recursive=True):
        total += find_todos(markdown_file)

    print(f"Todo entries: {total}")

if __name__ == "__main__":
    # read args otherwise use './docs' as default
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        if not os.path.isdir(folder):
            print(f"Error: {folder} is not a directory", file=sys.stderr)
            sys.exit(1)
        find_all_todos(sys.argv[1])
    else:
        find_all_todos('./docs')