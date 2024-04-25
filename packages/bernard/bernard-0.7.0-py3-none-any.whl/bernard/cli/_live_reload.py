"""
Live reload of code works the following way:

- There is a parent process that is just in charge of waiting for the child to
  die and then start it again, infinitely.
- The child process will start as usual and then look at its modules in order
  to watch them for changes. In case anything changes, then a small timeout
  is awaited then the process is exited with a special status code. When the
  parent picks this status code, it restarts the process.
"""

import asyncio
import contextlib
import logging
import subprocess
import sys
import sysconfig
from itertools import chain
from os import environ
from pathlib import Path

from watchdog.events import EVENT_TYPE_CLOSED, EVENT_TYPE_OPENED, FileSystemEventHandler
from watchdog.observers import Observer

from bernard.conf import list_config_files, settings

logger = logging.getLogger("bernard.cli")

FORBIDDEN_DIRS = {Path(x).absolute() for x in [*sysconfig.get_paths().values()]}


def _list_module_dirs():
    """
    List directory of modules
    """
    for m in sys.modules.values():
        with contextlib.suppress(AttributeError):
            yield from (Path(x).absolute() for x in m.__path__)


def _list_config_dirs():
    """
    List directories holding config files
    """
    yield from (Path(x).parent.absolute() for x in list_config_files())


# noinspection PyUnresolvedReferences
def _list_syntax_error():
    """
    If we're going through a syntax error, add the directory of the error to
    the watchlist.
    """
    _, e, _ = sys.exc_info()
    if isinstance(e, SyntaxError) and hasattr(e, "filename"):
        yield Path(e.filename).parent.absolute()


def list_dirs():
    """
    List all directories known to hold project code.
    """

    return {
        x
        for x in chain(
            _list_config_dirs(),
            _list_module_dirs(),
            _list_syntax_error(),
        )
        if not any(y in FORBIDDEN_DIRS for y in x.parents)
    }


_reloading = False


def exit_for_reload():
    """
    This triggers an exit with the appropriate signal for the parent to reload
    the code.
    """
    global _reloading

    if _reloading:
        return

    _reloading = True

    logger.warning("Reloading!")
    sys.exit(settings.CODE_RELOAD_EXIT)


class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop = asyncio.get_event_loop()

    def on_any_event(self, event):
        if event.event_type in {EVENT_TYPE_OPENED, EVENT_TYPE_CLOSED}:
            return

        if event.is_directory:
            return

        file_path = event.src_path

        if file_path.endswith(".py"):
            self._loop.call_later(settings.CODE_RELOAD_DEBOUNCE, exit_for_reload)


async def start_child():
    """
    Start the child process that will look for changes in modules.
    """
    logger.info("Started to watch for code changes")

    watched_dirs = list_dirs()

    observer = Observer()
    event_handler = CodeChangeHandler()

    for dir_name in sorted(str(x) for x in watched_dirs):
        observer.schedule(event_handler, dir_name, recursive=False)

    try:
        observer.start()
    except OSError as e:
        if e.errno == 24:
            logger.exception(
                "Too many files to watch. Try to increase your limit: "
                "echo 256 > /proc/sys/fs/inotify/max_user_instances"
            )
        raise

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def start_parent():
    """
    Start the parent that will simply run the child forever until stopped.
    """
    with contextlib.suppress(KeyboardInterrupt):
        while True:
            args = [sys.executable, *sys.argv]
            new_environ = environ.copy()
            new_environ["_IN_CHILD"] = "yes"
            ret = subprocess.call(args, env=new_environ)  # noqa: S603

            if ret != settings.CODE_RELOAD_EXIT:
                return ret
