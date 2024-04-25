import asyncio
import logging
from typing import TYPE_CHECKING, List, Optional, Tuple

from bernard.conf import settings
from bernard.utils import import_class

from .loaders import BaseIntentsLoader, IntentDict
from .utils import LocalesFlatDict

if TYPE_CHECKING:
    from bernard.engine.request import Request


logger = logging.getLogger(__name__)


class IntentsDb(LocalesFlatDict):
    """
    Database of intents. In the future it will handle different langs but right
    now it only handles one.
    """

    def __init__(self):
        super().__init__()
        self.loaders: List[BaseIntentsLoader] = []
        self._init_t = None

    async def ensure_loaded(self):
        if not self._init_t:
            logger.info("Loading intents")
            self._init_t = asyncio.get_running_loop().create_task(self._init_loaders())

        await self._init_t

    async def _init_loaders(self) -> None:
        """
        Gets loaders from conf, make instances and subscribe to them.
        """
        for loader in settings.I18N_INTENTS_LOADERS:
            loader_class = import_class(loader["loader"])
            instance = loader_class()
            instance.on_update(self.update)
            await instance.load(**loader["params"])

    def update(self, new_data: IntentDict):
        """
        Receive an update from the loaders.
        """
        for locale, data in new_data.items():
            if locale not in self.dict:
                self.dict[locale] = {}

            self.dict[locale].update(data)

    async def get(self, key: str, locale: Optional[str]) -> List[Tuple[str, ...]]:
        """
        Get a single set of intents.
        """
        await self.ensure_loaded()

        locale = self.choose_locale(locale)
        logger.info("Getting intent %s for locale %s", key, locale)

        return self.dict[locale][key]


class Intent:
    """
    Represents an intent to be resolved later.
    """

    def __init__(self, db: Optional[IntentsDb], key: str):
        self.db = db
        self.key = key

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.key == other.key

    def __repr__(self):
        return f"Intent({self.key!r})"

    # noinspection PyUnusedLocal
    async def strings(
        self, request: Optional["Request"] = None
    ) -> List[Tuple[str, ...]]:
        """
        For the given request, find the list of strings of that intent. If the
        intent does not exist, it will raise a KeyError.
        """
        await self.db.ensure_loaded()

        if request:
            locale = await request.get_locale()
        else:
            locale = None

        return await self.db.get(self.key, locale)


class IntentsMaker:
    """
    Utility class to be used as singleton and produce Intents objects easily
    from anywhere in the code.
    """

    def __init__(self, db: IntentsDb = None):
        self.db = db

        if not self.db:
            self._refresh_intents_db()

    def _refresh_intents_db(self):
        """
        Re-read the config and re-generate the intents DB.
        """
        self.db = IntentsDb()

    def __getattr__(self, key: str) -> Intent:
        """
        Generate an intent. Use it this way:

        >>> i = IntentsMaker()
        >>> print(await i.FOO.strings())
        """
        return Intent(self.db, key)
