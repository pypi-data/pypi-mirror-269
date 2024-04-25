import re
import types
from pathlib import Path
from typing import Any

CONFIG_ATTR = re.compile(r"^[A-Z](?:_?[A-Z0-9]+)*$")


class Settings(dict):
    """
    This object handles settings loaded from a pure Python file.
    """

    def __getattr__(self, attr: str) -> Any:
        """
        Return a config value. Get it from the internal dict.

        :param attr: Name of the config value you want
        """
        try:
            return self[attr]
        except KeyError as ke:
            msg = f"Config has no '{ke.args[0]}'"
            raise AttributeError(msg) from None

    def __setattr__(self, attr: str, value: Any) -> None:
        """
        Define a configuration value. Internally, it is stored as a dictionary
        entry.

        :param attr: Key to save
        :param value: Value to put
        """
        self[attr] = value

    def _load(self, file_path: str | Path) -> None:
        """
        Load the configuration from a plain Python file. This file is executed
        on its own.

        Only keys matching the CONFIG_ATTR will be loaded. Basically, it's
        CONFIG_KEYS_LIKE_THIS.

        :param file_path: Path to the file to load
        """
        # noinspection PyUnresolvedReferences
        module_ = types.ModuleType("settings")
        module_.__file__ = file_path

        try:
            with Path(file_path).open(encoding="utf-8") as f:
                exec(  # noqa: S102
                    compile(f.read(), file_path, "exec"),
                    module_.__dict__,
                )
        except OSError as e:
            e.strerror = f"Unable to load configuration file ({e.strerror})"
            raise

        for key in dir(module_):
            if CONFIG_ATTR.match(key):
                self[key] = getattr(module_, key)


class LazySettings:
    """
    This object lazily loads the settings at first access.

    It works like `Settings`, except that instead of calling the `_load()`
    method, specify a list of files to load as argument.
    """

    def __init__(self, get_files):
        """
        Initialize internal cache.
        """
        self.__dict__.update(
            {
                "__settings": None,
                "_get_files": get_files,
            }
        )

    @property
    def _settings(self) -> Settings:
        """
        Return the actual settings object, or create it if missing.
        """
        if self.__dict__["__settings"] is None:
            self.__dict__["__settings"] = Settings()
            for file_path in self._get_files():
                if file_path:
                    # noinspection PyProtectedMember
                    self.__dict__["__settings"]._load(file_path)
        return self.__dict__["__settings"]

    def _reload(self) -> None:
        """
        Delete the inner settings object so it gets reloaded.
        """
        self.__dict__["__settings"] = None

    def __getattr__(self, key: str) -> Any:
        """
        Proxy to `Settings.__getattr__`
        """
        return getattr(self._settings, key)

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Proxy to `Settings.__setattr__`
        """
        return setattr(self._settings, key, value)
