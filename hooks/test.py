from markdown.extensions import Extension  # type: ignore
from markdown.preprocessors import Preprocessor  # type: ignore
from markdown.postprocessors import Postprocessor  # type: ignore
from pymdownx.snippets import SnippetExtension, SnippetPreprocessor  # type: ignore
from pymdownx.snippets import DEFAULT_URL_SIZE,  DEFAULT_URL_TIMEOUT
from pathlib import Path
import os
from pathlib import Path
from mkdocs.config.defaults import MkDocsConfig

ROOT_DIR = Path(__file__).parent.parent

def on_config(config: MkDocsConfig, **kwargs):
    if 'pymdownx.snippets' in config['markdown_extensions']:
        config['markdown_extensions'].remove('pymdownx.snippets')
    config.markdown_extensions.append(WLExtension(config))
    return config


def on_post_build(config, **kwargs):
    print(config)


class WLExtension(Extension):

    def __init__(self, mkconfig):
        self.mkconfig = mkconfig

        if 'pymdownx.snippets' in self.mkconfig.mdx_configs:
            bpath = self.mkconfig.mdx_configs['pymdownx.snippets']\
                .get('base_path', ['.', 'includes'])

            excluded_dirs = ['.', '__', 'site', 'env', 'venv']

            for root, dirs, _ in os.walk('.'):
                dirs[:] = [d for d in dirs if not
                           any(d.startswith(exclude) for exclude in excluded_dirs)]

                bpath.extend(os.path.relpath(
                    os.path.join(root, d), '.') for d in dirs)

            self.mkconfig.mdx_configs['pymdownx.snippets']['base_path'] = bpath

    def extendMarkdown(self, md):  # noqa: N802

        self.md = md
        md.registerExtension(self)

        # Snippet extension preprocessor
        sc = self.mkconfig.mdx_configs['pymdownx.snippets']
        sc.setdefault('dedent_subsections', True)
        sc.setdefault('url_request_headers', {})
        sc.setdefault('url_timeout', DEFAULT_URL_TIMEOUT)
        sc.setdefault('url_max_size', DEFAULT_URL_SIZE)
        sc.setdefault('url_download', True)
        sc.setdefault('auto_append', [])
        sc.setdefault('check_paths', True)
        sc.setdefault('encoding', 'utf-8')
        sc.setdefault('restrict_base_path', True)
        sc.setdefault('base_path', ['.', 'includes'])

        sp = SnippetPreprocessor(sc, md)
        self.wlpp = WLPreprocessor(self.mkconfig, sp)
        md.preprocessors.register(self.wlpp, 'wl-pp', 50)


class WLPreprocessor(Preprocessor):
    def __init__(self, mkconfig, snippet_preprocessor):
        self.mkconfig = mkconfig
        self.snippet_preprocessor = snippet_preprocessor

    def run(self, lines):
        _lines = self.snippet_preprocessor.run(lines)
        return _lines
