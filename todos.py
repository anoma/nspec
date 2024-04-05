import os
import glob

def report_todo_entries(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i, line in enumerate(lines, start=1):
            if line.strip().startswith("!!! todo"):
                # Report the todo entry
                # Prepare the message by joining this line and the next few lines until they're not indented
                message = line.strip()
                for j in range(i+1, min(i+4, len(lines))):  # Look ahead a few lines for the full message
                    next_line = lines[j].strip()
                    if next_line.startswith('    '):  # Assuming continuation lines are indented
                        message += ' ' + next_line[4:]  # Append with a space, remove indentation
                    else:
                        break  # Stop if the next line is not a continuation of the TODO
                message = message  # Truncate to 140 chars if longer

                print(f"{os.path.abspath(file_path)}:{i}:1: {message}")

def report_all_todos_in_directory(directory_path):
    for markdown_file in glob.glob(os.path.join(directory_path, '**', '*.md'), recursive=True):
        report_todo_entries(markdown_file)

# Replace './docs' with the path to your specific directory if different
report_all_todos_in_directory('./docs')
