"""
Settings management.

This module is really inspired by the Django and the Sanic config systems,
thanks to their teams.
"""

import os
from pathlib import Path
from typing import List

from .loader import LazySettings

ENVIRONMENT_VARIABLE = "BERNARD_SETTINGS_FILE"


def list_config_files() -> List[Path]:
    """
    This function returns the list of configuration files to load.

    This is a callable so the configuration can be reloaded with files that
    changed in between.
    """

    out = [Path(__file__).parent / "default_settings.py"]

    if env_path := os.getenv(ENVIRONMENT_VARIABLE):
        out.append(Path(env_path))

    return out


settings = LazySettings(list_config_files)
