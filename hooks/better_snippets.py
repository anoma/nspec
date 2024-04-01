

import logging
import os
from mkdocs.config.defaults import MkDocsConfig

log: logging.Logger = logging.getLogger('mkdocs')


def on_pre_build(config: MkDocsConfig):
    if 'pymdownx.snippets' in config.mdx_configs:
        base_path = ['.', 'includes']  # default base path
        excluded_dirs = ['.', '__', 'site', 'env', 'venv']
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not any(
                d.startswith(exclude) for exclude in excluded_dirs)]
            base_path.extend(os.path.relpath(
                os.path.join(root, d), '.') for d in dirs)
        config.mdx_configs['pymdownx.snippets']['base_path'] = base_path
