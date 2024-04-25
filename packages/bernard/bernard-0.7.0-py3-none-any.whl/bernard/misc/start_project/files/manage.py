#!/usr/bin/env python3

from os import environ
from pathlib import Path
from sys import path as py_path
from sys import stderr

ROOT = Path(__file__).parent

environ.setdefault(
    "BERNARD_SETTINGS_FILE",
    str(ROOT / "src/__project_name_snake__/settings.py"),
)


if __name__ == "__main__":
    try:
        py_path.append(str(ROOT / "src"))
        from bernard.misc.main import main

        main()
    except ImportError:
        print(  # noqa: T201
            "Could not import BERNARD. Is your environment correctly " "configured?",
            file=stderr,
        )
        exit(1)
