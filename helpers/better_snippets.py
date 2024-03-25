

import logging
import os
import re
import shutil
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

log: logging.Logger = logging.getLogger('mkdocs')

def on_pre_build(config):
  if 'pymdownx.snippets' in config.mdx_configs:
    base_path = ['.', 'includes'] # default base path
                    
    rel_dirs = [] # relative directories to the root
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs \
                   if not d.startswith('.') and \
                     not d.startswith('__') and \
                     not d.startswith('site') and \
                    not d.startswith('env') and \
                    not d.startswith('venv')
        ]
        for d in dirs:
            rel_dir = os.path.relpath(os.path.join(root, d), '.')
            print(rel_dir)
            base_path.append(rel_dir)

    config.mdx_configs['pymdownx.snippets']['base_path'] = base_path
    print(f"base_path: {base_path}")