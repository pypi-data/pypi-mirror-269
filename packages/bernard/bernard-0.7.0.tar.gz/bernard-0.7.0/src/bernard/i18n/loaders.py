import asyncio
import contextlib
import csv
import logging
import os.path
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union

from watchdog.events import EVENT_TYPE_CLOSED, EVENT_TYPE_OPENED, FileSystemEventHandler
from watchdog.observers import Observer

from bernard.conf import settings

logger = logging.getLogger("bernard.i18n.loaders")


TransDict = Dict[Optional[str], List[Tuple[str, str]]]
IntentDict = Dict[Optional[str], Dict[str, List[Tuple[str, ...]]]]

_pending_t = set()


class LiveFileLoaderMixin:
    """
    A mixin to help detecting live changes in translations and update them
    directly when saved.
    """

    THING = "file"

    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super().__init__(*args, **kwargs)
        self._event = asyncio.Event()
        self._file_path = None
        self._running = False
        self._locale = None
        self._kwargs = {}

    async def _load(self):
        """
        In this method you load the data from your file. You have to implement
        it. You can do whatever you want with it.
        """
        raise NotImplementedError

    async def _watch(self):
        """
        Start the watching loop.
        """
        logger.info('Watching %s "%s"', self.THING, self._file_path)

        while await self._event.wait() and self._running:
            self._event.clear()
            await self._load()
            logger.info('Reloading changed %s from "%s"', self.THING, self._file_path)

    def _watchdog(self):
        # noinspection PyMethodParameters
        class Handler(FileSystemEventHandler):
            def on_any_event(_self, event):
                if event.event_type in {EVENT_TYPE_OPENED, EVENT_TYPE_CLOSED}:
                    return

                self._event.set()

        handler = Handler()
        observer = Observer()
        observer.schedule(handler, self._file_path)
        observer.start()

    async def start(self, file_path, locale=None, kwargs=None):
        """
        Set up the watching utilities, start the loop and load data a first
        time.
        """
        self._file_path = os.path.realpath(file_path)
        self._locale = locale

        if kwargs:
            self._kwargs = kwargs

        await self._load()

        if settings.I18N_LIVE_RELOAD:
            loop = asyncio.get_event_loop()

            self._running = True
            self._watchdog()

            t = loop.create_task(self._watch())
            _pending_t.add(t)
            t.add_done_callback(_pending_t.discard)


class BaseTranslationLoader:
    """
    Base skeleton for a translation loader.

    Loaders must have an asynchronous `load` function that will be called with
    kwargs only. This function must load the translations and trigger an
    update event. It must NOT finish before the update is done.
    """

    def __init__(self):
        self.listeners: list[Callable[[TransDict], None]] = []

    def on_update(self, cb: Callable[[TransDict], None]) -> None:
        """
        Registers an update listener

        :param cb: Callback that will get called on update
        """
        self.listeners.append(cb)

    def _update(self, data: TransDict, *args, **kwargs):
        """
        Propagate updates to listeners

        :param data: Data to propagate
        """
        for listener in self.listeners:
            listener(data, *args, **kwargs)

    async def load(self, **kwargs) -> None:
        """
        Starts the load cycle. Data must be loaded at least once before this
        function finishes.
        """
        raise NotImplementedError


class CsvTranslationLoader(LiveFileLoaderMixin, BaseTranslationLoader):
    """
    Loads data from a CSV file
    """

    THING = "CSV translation"

    async def _load(self):
        """
        Load data from a Excel-formatted CSV file.
        """
        flags = self._kwargs.get("flags")

        if not flags:
            flags = {1: {}}

        cols = {k: [] for k in flags}

        def read():
            with Path(self._file_path).open(newline="", encoding="utf-8") as f:
                reader = csv.reader(f)

                for row in reader:
                    for _i, _col in cols.items():
                        try:
                            val = row[_i].strip()
                        except IndexError:
                            pass
                        else:
                            if val:
                                _col.append((row[0], val))

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, read)

        for i, col in cols.items():
            self._update({self._locale: col}, flags[i])

        logger.info('Loaded %s from "%s"', self.THING, self._file_path)

    async def load(self, file_path, locale=None, flags=None):
        """
        Start the loading/watching process
        """
        await self.start(file_path, locale, {"flags": flags})


class BaseIntentsLoader:
    """
    Base skeleton for an intents loader.

    Loaders must have an asynchronous `load` function that will be called with
    kwargs only. This function must load the translations and trigger an
    update event. It must NOT finish before the update is done.
    """

    def __init__(self):
        self.listeners: list[Callable[[IntentDict], None]] = []

    def on_update(self, cb: Callable[[IntentDict], None]) -> None:
        """
        Registers an update listener

        :param cb: Callback that will get called on update
        """
        self.listeners.append(cb)

    def _update(self, data: IntentDict):
        """
        Propagate updates to listeners

        :param data: Data to propagate
        """
        for listener in self.listeners:
            listener(data)

    async def load(self, **kwargs) -> None:
        """
        Starts the load cycle. Data must be loaded at least once before this
        function finishes.
        """
        raise NotImplementedError


ColRanges = List[
    Union[
        int,
        Tuple[int, Optional[int]],
    ]
]


def extract_ranges(row, ranges: ColRanges) -> List[str]:
    """
    Extracts a list of ranges from a row:

    - If the range is an int, just get the data at this index
    - If the range is a tuple of two ints, use them as indices in a slice
    - If the range is an int then a None, start the slice at the int and go
      up to the end of the row.
    """
    out = []

    for r in ranges:
        if isinstance(r, int):
            r = (r, r + 1)

        if r[1] is None:
            r = (r[0], len(row))

        out.extend(row[r[0] : r[1]])

    return [x for x in (y.strip() for y in out) if x]


class CsvIntentsLoader(LiveFileLoaderMixin, BaseIntentsLoader):
    """
    Load intents from a CSV
    """

    THING = "CSV intents"

    async def _load(self):
        """
        Load data from a Excel-formatted CSV file.
        """
        key = self._kwargs["key"]
        pos = self._kwargs["pos"]
        neg = self._kwargs["neg"]

        data = {}

        def read():
            with Path(self._file_path).open(newline="", encoding="utf-8") as f:
                reader = csv.reader(f)

                for row in reader:
                    with contextlib.suppress(IndexError):
                        data[row[key]] = [
                            *data.get(row[key], []),
                            tuple(extract_ranges(row, [pos, *neg])),
                        ]

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, read)

        self._update({self._locale: data})

    async def load(
        self,
        file_path,
        locale=None,
        key: int = 0,
        pos: int = 1,
        neg: Optional[ColRanges] = None,
    ):
        """
        Start the loading/watching process
        """
        if neg is None:
            neg: ColRanges = [(2, None)]

        await self.start(
            file_path,
            locale,
            kwargs={
                "key": key,
                "pos": pos,
                "neg": neg,
            },
        )
