import os

# Specify the folder path
folder_path = "./docs/arch/system/state/resource_machine/"

# Walk through each directory and its subdirectories
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        path = (os.path.join(root, filename))
        juvix_import = f"import {path}".replace("./docs/", "").replace("/", ".").replace(".juvix.md", "") + ";"
        print(juvix_import)
        # Check if the file is a markdown file
        # if filename.endswith(".juvix.md"):
            # Construct full file path  