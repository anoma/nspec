#

import os
import re
import shutil
from pathlib import Path

# Dummy replacements for directories and files (for demonstration purposes)


def prompt_boolean(prompt, allow_all=False):
    """Prompt user for a yes/no response, optionally allowing for 'yes all'/'no all'"""
    valid_responses = {"yes": True, "y": True, "no": False, "n": False}
    if allow_all:
        valid_responses.update(
            {
                "yes all": "all_yes",
                "y all": "all_yes",
                "ya": "all_yes",
                "yesall": "all_yes",
                "na": "all_no",
                "no all": "all_no",
                "n all": "all_no",
            }
        )  # type: ignore

    while True:
        response = input(prompt).strip().lower()
        if response in valid_responses:
            return valid_responses[response]
        print("Invalid input. Please enter 'yes', 'no', 'yes all', or 'no all'.")


def to_snake(name):
    # Convert to snake case
    if "Package.juvix" in name:
        return name
    new_name = re.sub(
        r"(.)([A-Z][a-z]+)", r"\1_\2", name
    )  # Handle transition from lower/upper to Upper/lower case
    new_name = re.sub(
        r"([a-z0-9])([A-Z])", r"\1_\2", new_name
    )  # Handle transition from any lower/digit to upper case
    new_name = new_name.replace("-", "_")
    while "__" in new_name:
        new_name = new_name.replace("__", "_")
    new_name = new_name.replace("architecture_2", "node_architecture")
    new_name = new_name.replace("architecture_1", "system_architecture")
    # Remove leading and trailing underscores
    new_name = new_name.strip("_")
    # Remove "/_" and "_/" from the name
    new_name = new_name.replace("/_", "/").replace("_/", "/")
    return new_name.lower()


def rename_dirs_recursive(root_dir):
    replacements_dir = {}
    replacements_file = {}

    root_directory = Path(root_dir)
    skipping = []
    for path_object in root_directory.rglob("*"):
        old_path = path_object.as_posix()
        snake_path = to_snake(old_path)
        cond = any(
            skip_pattern in old_path
            for skip_pattern in [
                ".juvix-build",
                ".config",
                "tara",
                "docs/assets",
                "docs/.git",
                "docs/images",
            ]
        )
        if not cond and old_path != snake_path:
            if path_object.exists():
                if path_object.is_file():
                    replacements_file[old_path] = snake_path
                elif path_object.is_dir():
                    replacements_dir[old_path] = snake_path
                else:
                    print("Unknown file type:", old_path)
                    continue
            # path_object.rename()
        else:
            skipping.append(old_path)

    def renaming(proceed_rename=True):
        all_replacements = []
        if proceed_rename == "all_no":
            return  # Exit early if 'no all'

        proceed_directories = (
            proceed_rename
            if proceed_rename in ["all_yes", "all_no"]
            else prompt_boolean(
                "Proceed with renaming directories? (yes/no/yes all/no all): ",
                allow_all=True,
            )
        )

        if proceed_directories in [True, "all_yes"]:
            all_replacements.extend(replacements_dir.items())

        proceed_files = (
            proceed_directories
            if proceed_directories in ["all_yes", "all_no"]
            else prompt_boolean(
                "Proceed with renaming files? (yes/no/yes all/no all): ", allow_all=True
            )
        )

        if proceed_files in [True, "all_yes"]:
            all_replacements.extend(replacements_file.items())

        for old_path, new_path in all_replacements:
            if Path(new_path).exists():
                print(f"Path exists: {new_path}")
                continue

            rename_file = (
                proceed_files
                if proceed_files in ["all_yes", "all_no"]
                else prompt_boolean(
                    f"Rename {old_path} -> {new_path}? (yes/no/yes all/no all): "
                )
            )

            if rename_file in [True, "all_yes"]:
                path_object = Path(old_path)
                new_path_obj = Path(new_path)

                if path_object.is_dir():
                    new_path_obj.mkdir(parents=True, exist_ok=True)
                    if not new_path_obj.exists():
                        print(f"Failed to create directory: {new_path}")
                    # Can add logic to delete old path if needed

                elif path_object.is_file():
                    shutil.copy2(old_path, new_path)
                    if not new_path_obj.exists():
                        print(f"Failed to rename file: {new_path}")

    proceed_rename = prompt_boolean(
        "Proceed with renaming? (yes/no/yes all/no all): ", allow_all=True
    )
    renaming(proceed_rename)

    def update_config_mkdocs(update_mkdocs=True):
        if update_mkdocs in ["all_no"]:
            return
        if update_mkdocs in [True, "all_yes"]:
            content = ""
            with open("mkdocs.yml", "r") as f:
                content = f.read()
            with open("mkdocs.yml", "w") as f:
                for _old_string, _new_string in [
                    *replacements_dir.items(),
                    *replacements_file.items(),
                ]:
                    old_string = _old_string.replace("docs/", "")
                    new_string = _new_string.replace("docs/", "")
                    # Inside the content of the file, we may need to replace suffixes of
                    # the old string by the corresponding suffixes of the new string.
                    # For example, if the old string is "A/B/C/D.md" and the new string
                    # is "nA/nB/nC/nD.md", then we need to replace:
                    # - "A/B/C/D.md" by "nA/nB/nC/nD.md"
                    # - "B/C/D.md" by "nB/nC/nD.md"
                    # - "C/D.md" by "nC/nD.md"
                    # - "D.md" by "nD.md"
                    old_string_parts = old_string.split("/")
                    new_string_parts = new_string.split("/")
                    for i in range(len(old_string_parts)):
                        old_suffix = "/".join(old_string_parts[i:])
                        new_suffix = "/".join(new_string_parts[i:])
                        content = content.replace(old_suffix, new_suffix)
                f.write(content)

    proceed_content_update = prompt_boolean(
        "Proceed with updating mkdocs.yml? (yes/no/yes all/no all): ", allow_all=True
    )
    update_config_mkdocs(proceed_content_update)

    def delete_old_folders(proceed=True):
        if proceed in ["all_no"]:
            return
        delete_old_dirs = (
            proceed
            if proceed in ["all_yes", "all_no"]
            else prompt_boolean(
                "Delete old directories? (yes/no/yes all/no all): ", allow_all=True
            )
        )
        if delete_old_dirs in [True, "all_yes"]:
            for _old_path, _ in replacements_dir.items():
                old_path = Path(_old_path)
                if old_path.exists():
                    shutil.rmtree(old_path)
                    print(f"Deleted: {old_path}")

    proceed_delete_old_dirs = prompt_boolean(
        "Proceed with deleting old dirs? (yes/no/yes all/no all): ", allow_all=True
    )
    delete_old_folders(proceed_delete_old_dirs)

    print("Updating content of markdown files...")
    # Iterate over markdown files in the 'docs' directory
    process = True
    for path_object in root_directory.rglob("**/*.md"):
        path = path_object.as_posix()
        cond = any(
            skip_pattern in path
            for skip_pattern in [
                ".juvix-build",
                ".config",
                "tara",
                "docs/assets",
                "docs/.git",
                "docs/images",
            ]
        )
        if cond:
            continue

        process = (
            process
            if process in ["all_yes", "all_no"]
            else prompt_boolean(
                f"Review: {path_object.as_posix()}\nProcess? (yes/no/yes all/no all):",
                allow_all=True,
            )
        )
        if process in [False]:
            continue
        if process in ["all_no"]:
            break
        content = ""
        fp = path_object.as_posix()

        # Read file content
        with open(fp, "r") as file:
            content = file.read()

        # Replace content
        new_content = content
        for _old_string, _new_string in [
            *replacements_file.items(),
            *replacements_dir.items(),
        ]:
            # remove the leading './' from the path or "docs/" from the paths
            old_string = _old_string.replace("docs/", "")
            new_string = _new_string.replace("docs/", "")
            old_string_parts = old_string.split("/")
            new_string_parts = new_string.split("/")
            for i in range(len(old_string_parts)):
                old_suffix = "/".join(old_string_parts[i:])
                new_suffix = "/".join(new_string_parts[i:])
                new_content = new_content.replace(old_suffix, new_suffix)
        if new_content == content:
            continue

        # Write back if there are any changes
        with open(fp, "w") as file:
            file.write(new_content)
        cont = (
            process
            if process in ["all_yes", "all_no"]
            else prompt_boolean("Continue? (yes/no/yes all/no all): ", allow_all=True)
        )
        if cont in ["all_no"]:
            break


if __name__ == "__main__":
    root_directory = "./docs/"  # Specify the top directory here
    if Path(root_directory).exists():
        rename_dirs_recursive(root_directory)
