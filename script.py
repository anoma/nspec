import os
import glob

def convert_todo_syntax(file_path):
    new_lines = []  # Store the new lines here
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        inside_todo_block = False
        for line in lines:
            if line.strip().startswith(">"):
                if inside_todo_block:
                    # Finish the previous block if we're already inside a TODO block
                    new_lines.append('\n')  # Add an extra line for clarity
                # Start a new TODO block
                inside_todo_block = True
                new_lines.append("!!! quote\n\n")
                new_lines.append(f"    {line.strip()[1:]}\n")
            elif inside_todo_block and (line.strip() == "" or line.startswith('>')):
                # Continue the TODO block if the next line is also indented or blank
                new_lines.append(f"    {line.strip()[1:]}\n")
            else:
                # If we hit a line that doesn't continue the TODO, we end the block
                inside_todo_block = False
                new_lines.append(line)

    # Rewrite the file with the modified lines
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

def convert_all_markdowns_in_directory(directory_path):
    # Use glob with ** to match all markdown files recursively
    for markdown_file in glob.glob(os.path.join(directory_path, '**', '*.md'), recursive=True):
        print(f'Converting: {markdown_file}')
        convert_todo_syntax(markdown_file)
    print('All markdown files have been converted.')

# Replace './docs' with the path to your specific directory if different
convert_all_markdowns_in_directory('./docs')