import os
import shutil
from pathlib import Path
from typing import Set

# Move images contained in docs all over into the solver and move them
# docs/assets/images using pathlib Define the source and destination directories

source = Path('docs')
destination = Path('docs/images')
destination.mkdir(parents=True, exist_ok=True)

# Move all images from the source directory to the destination directory
filenames: Set[str] = set()
for root, dirs, files in os.walk(source):
    for file in files:
        if file.endswith('.png') or file.endswith('.jpg') or \
        file.endswith('.jpeg') or file.endswith('.svg') or \
        file.endswith('.gif'):
            if  'docs/assets' in root or "docs/images" in root:
                continue
            move = False
            if not file in filenames:
                filenames.add(file)
                move = True
            else:
                filepath = Path(root) / file
                if filepath.read_bytes() != (destination / file).read_bytes():
                        ask = input(f'File {file} already exists in the destination directory. Do you want to overwrite it? (y/n): ')
                        if ask == 'y':
                            move = True
                        else:
                            move = False
            if move:
                print(f'Moving {file} from {root}')
                shutil.move(Path(root) / file, destination / file)