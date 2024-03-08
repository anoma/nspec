from datetime import datetime
import os
from pathlib import Path
import subprocess
import logging

log = logging.getLogger('mkdocs')


def define_env(env):
    env.variables.version = "v2"
    env.variables.last_updated = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")

    @env.macro
    def date(d):
        return datetime.strptime(d, '%Y-%m-%d')
