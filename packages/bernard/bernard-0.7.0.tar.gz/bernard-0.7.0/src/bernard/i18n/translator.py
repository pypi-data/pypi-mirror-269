import asyncio
import logging
from collections import defaultdict
from itertools import zip_longest
from random import SystemRandom
from string import Formatter
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Tuple,
    Union,
)

from bernard.conf import settings
from bernard.i18n.loaders import BaseTranslationLoader, TransDict
from bernard.utils import import_class

from ._formatter import I18nFormatter
from .utils import LocalesDict

if TYPE_CHECKING:
    from bernard.engine.request import Request


random = SystemRandom()
logger = logging.getLogger(__name__)


Flags = Dict[str, str]


class TranslationError(Exception):
    """
    That is the base translation error class
    """


class MissingTranslationError(TranslationError):
    """
    Raised when a translation that was asked does not exist
    """


class MissingParamError(TranslationError):
    """
    Raised if a translation needs parameters that can't be found
    """


class TransItem(NamedTuple):
    """
    This is a single "item of translation". Typically, it comes from the CSV.

    It's a de-normalized representation of translations. There is 3 properties
    today, but it might become more in the future.

    - `key` is the translation key
    - `index` is the number of the message in case you're doing a multipart
      message (from 1 to the infinite)
    - `value` is the raw text value
    - `flags` are key/values that will be compared to the translation context
      for the current request. Translations will be chosen between items of
      equal flag "score".
    """

    key: str
    index: int
    value: str
    flags: Flags

    def score(self, flags: Flags) -> int:
        """
        Counts how many of the flags can be matched
        """
        score = 0

        for k, v in flags.items():
            if self.flags.get(k) == v:
                score += 1

        return score


class Sentence:
    """
    A single sentence. The main goal of this class is to provide an easy way to
    get a random sentence from the list and to see if the list is valid.
    """

    def __init__(self):
        self.items: List[TransItem] = []

    def best_for_flags(self, flags: Flags) -> List[TransItem]:
        """
        Given `flags`, find all items of this sentence that have an equal
        matching score and put them in a list.
        """
        best_score: int = 0
        best_list: List[TransItem] = []

        for item in self.items:
            score = item.score(flags)

            if score == best_score:
                best_list.append(item)
            elif score > best_score:
                best_list = [item]
                best_score = score

        return best_list

    def render(self, flags: Flags) -> str:
        """
        Chooses a random sentence from the list and returns it.
        """
        return random.choice(self.best_for_flags(flags)).value

    def append(self, item: TransItem):
        """
        Add an item to the list. No checks are made, it's assumed that the
        object is consistent with the others in the list.
        """
        self.items.append(item)

    def check(self):
        """
        Checks that the list is not empty.
        """
        return bool(self.items)

    def update(self, new: "Sentence", flags: Flags):
        """
        Erase items with the specified flags and insert the new items from
        the other sentence instead.
        """
        items = [i for i in self.items if i.flags != flags]
        items.extend(new.items)
        self.items = items


class SentenceGroup:
    """
    That's a group of sentences, aka a "step" in a conversation that might get
    split into several messages at the will of the translator.

    It will automatically group items into sentences of the same index, however
    you need at least one item for each sentence. In other words, if you try
    to add FOO+1 and FOO+3 it won't work.

    Order of insertion does not matter.
    """

    def __init__(self):
        self.sentences: List[Sentence] = []

    def render(self, flags: Flags) -> List[str]:
        """
        Returns a list of randomly chosen outcomes for each sentence of the
        list.
        """
        return [x.render(flags) for x in self.sentences]

    def append(self, item: TransItem):
        """
        Append an item to the list. If there is not enough sentences in the
        list, then the list is extended as needed.

        There is no control made to make sure that the key is consistent.
        """
        if not (1 <= item.index <= settings.I18N_MAX_SENTENCES_PER_GROUP):
            return

        if len(self.sentences) < item.index:
            for _ in range(len(self.sentences), item.index):
                self.sentences.append(Sentence())

        self.sentences[item.index - 1].append(item)

    def check(self):
        return len(self.sentences) and all(x.check() for x in self.sentences)

    def update(self, group: "SentenceGroup", flags: Flags) -> None:
        """
        This object is considered to be a "global" sentence group while the
        other one is flags-specific. All data related to the specified flags
        will be overwritten by the content of the specified group.
        """
        to_append = []

        for old, new in zip_longest(self.sentences, group.sentences):
            if old is None:
                old = Sentence()
                to_append.append(old)

            if new is None:
                new = Sentence()

            old.update(new, flags)

        self.sentences.extend(to_append)


class SortingDict:
    """
    A validating and sorting dictionary for translation items. The intended use
    is to append all your values to it and then to extract it to get only the
    valid keys out. Then you can discard this object.
    """

    def __init__(self):
        self.data: Dict[str, SentenceGroup] = defaultdict(lambda: SentenceGroup())

    def extract(self):
        """
        Extract only the valid sentence groups into a dictionary.
        """
        out = {}

        for key, group in self.data.items():
            out[key] = group

        return out

    def append(self, item: TransItem):
        """
        Append an item to the internal dictionary.
        """
        self.data[item.key].append(item)


class WordDictionary(LocalesDict):
    """
    That's where the actual translation happens. It stores all translations in
    memory, puts the parameters in place and so on.
    """

    def __init__(self):
        super().__init__()
        self.loaders: list[BaseTranslationLoader] = []
        self._init_t = None

    async def ensure_loaded(self):
        if not self._init_t:
            logger.info("Loading translations")
            self._init_t = asyncio.get_running_loop().create_task(self._init_loaders())

        await self._init_t

    async def _init_loaders(self) -> None:
        """
        This creates the loaders instances and subscribes to their updates.
        """
        for loader in settings.I18N_TRANSLATION_LOADERS:
            loader_class = import_class(loader["loader"])
            instance = loader_class()
            instance.on_update(self.update)
            await instance.load(**loader["params"])

    def parse_item(self, key, value, flags: Flags) -> Optional[TransItem]:
        """
        Parse an item (and more specifically its key).
        """
        parts = key.split("+")
        pure_key = parts[0]

        try:
            if len(parts) == 2:
                index = int(parts[1])
            elif len(parts) > 2:
                return None
            else:
                index = 1
        except (ValueError, TypeError):
            return None

        if index < 1:
            return None

        return TransItem(
            key=pure_key,
            index=index,
            value=value,
            flags=flags,
        )

    def update_lang(
        self, lang: Optional[str], data: List[Tuple[str, str]], flags: Flags
    ):
        """
        Update translations for one specific lang
        """
        sd = SortingDict()

        for item in (self.parse_item(x[0], x[1], flags) for x in data):
            if item:
                sd.append(item)

        if lang not in self.dict:
            self.dict[lang] = {}

        d = self.dict[lang]

        for k, v in sd.extract().items():
            if k not in d:
                d[k] = SentenceGroup()

            d[k].update(v, flags)

    def update(self, data: TransDict, flags: Flags):
        """
        Update all langs at once
        """
        for lang, lang_data in data.items():
            self.update_lang(lang, lang_data, flags)

    async def get(
        self,
        key: str,
        count: Optional[int] = None,
        formatter: Formatter | None = None,
        locale: str | None = None,
        params: Optional[Dict[str, Any]] = None,
        flags: Optional[Flags] = None,
    ) -> List[str]:
        """
        Get the appropriate translation given the specified parameters.

        :param key: Translation key
        :param count: Count for plurals
        :param formatter: Optional string formatter to use
        :param locale: Preferred locale to get the string from
        :param params: Params to be substituted
        :param flags: Flags to help choosing one version or the other
        """
        if params is None:
            params = {}

        if count is not None:
            msg = "Count parameter is not supported yet"
            raise TranslationError(msg)

        await self.ensure_loaded()

        locale = self.choose_locale(locale)

        try:
            group: SentenceGroup = self.dict[locale][key]
        except KeyError:
            msg = f'Translation "{key}" does not exist'
            raise MissingTranslationError(msg) from None

        try:
            trans = group.render(flags or {})
            out = []

            for line in trans:
                if not formatter:
                    out.append(line.format(**params))
                else:
                    out.append(formatter.format(line, **params))
        except KeyError as e:
            msg = f'Parameter "{e.args[0]}" missing to translate "{key}"'
            raise MissingParamError(msg) from None
        else:
            return out


class StringToTranslate:
    """
    That's a string to translate. It holds the parameters until it gets
    rendered.
    """

    LINE_SEPARATOR = "\n"

    def __init__(
        self,
        wd: WordDictionary,
        key: str,
        count: int | None = None,
        params: dict[str, Any] | None = None,
    ):
        if params is None:
            params = {}

        self.wd = wd
        self.key = key
        self.count = count
        self.params = params

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.key == other.key
            and self.count == other.count
            and self.params == other.params
        )

    def __repr__(self):
        parts = [repr(self.key)]

        if self.count is not None:
            parts.append(repr(self.count))

        for k, v in self.params.items():
            parts.append(f"{k}={v!r}")

        return "t({})".format(", ".join(parts))

    async def _resolve_params(
        self, params: Dict[str, Any], request: Optional["Request"]
    ):
        """
        If any StringToTranslate was passed as parameter then it is rendered
        at this moment.
        """
        out = {}

        for k, v in params.items():
            if isinstance(v, StringToTranslate):
                out[k] = await render(v, request)
            else:
                out[k] = v

        return out

    async def render(self, request=None):
        """
        Render the translation for the specified request. If no request is
        specified, do as good as possible.

        :param request: Bot request. No one knows what it's going to look like
                        so far.
        """
        return self.LINE_SEPARATOR.join(await self.render_list(request))

    # noinspection PyUnusedLocal
    async def render_list(self, request=None) -> List[str]:
        """
        Render the translation as a list if there is multiple strings for this
        single key.

        :param request: Bot request.
        """
        from bernard.middleware import MiddlewareManager

        await self.wd.ensure_loaded()

        if request:
            tz = await request.user.get_timezone()
            locale = await request.get_locale()
            flags = await request.get_trans_flags()
        else:
            tz = None
            locale = self.wd.list_locales()[0]
            flags = {}

        rp = MiddlewareManager.instance().get(
            "resolve_trans_params", self._resolve_params
        )

        resolved_params = await rp(self.params, request)

        f = I18nFormatter(self.wd.choose_locale(locale), tz)
        return await self.wd.get(
            self.key,
            self.count,
            f,
            locale,
            resolved_params,
            flags,
        )


class Translator:
    """
    That's the basic object that you use to produce translations.
    """

    def __init__(self, wd: Optional[WordDictionary] = None):
        """
        We need the word dictionary here in order to pass it to the string to
        translate when it will get rendered.

        :param wd: a configured WordDictionary
        """
        self.wd = wd  # type: WordDictionary

        if not self.wd:
            self._regenerate_word_dict()

    def _regenerate_word_dict(self):
        """
        Re-generate the word dict, if you need to.
        """
        self.wd = WordDictionary()

    def __getattr__(self, key: str) -> StringToTranslate:
        """
        Allow the `t.FOO` style.

        :param key: Key to get
        """
        return self(key)

    def __call__(
        self, key: str, count: Optional[int] = None, **params
    ) -> StringToTranslate:
        """
        Allow the `t('FOO')` style.

        :param key: Key to translate
        :param count: Count for plurals
        :param params: Params to substitute
        """
        return StringToTranslate(self.wd, key, count, params)


TransText = Union[StringToTranslate, str]


def serialize(text: TransText):
    """
    Takes as input either a string to translate either an actual string and
    transforms it into a JSON-serializable structure that can be reconstructed
    using `unserialize()`.
    """
    if isinstance(text, str):
        return {
            "type": "string",
            "value": text,
        }
    elif isinstance(text, StringToTranslate):
        return {
            "type": "trans",
            "key": text.key,
            "count": text.count,
            "params": text.params,
        }
    else:
        msg = f'Cannot accept type "{text.__class__.__name__}"'
        raise ValueError(msg)


def unserialize(wd: WordDictionary, text: Dict):
    """
    Transforms back a serialized value of `serialize()`
    """
    if not isinstance(text, Mapping):
        msg = "Text has not the right format"
        raise ValueError(msg)

    try:
        t = text["type"]

        if t == "string":
            return text["value"]
        elif t == "trans":
            if not isinstance(text["params"], Mapping):
                msg = "Params should be a dictionary"
                raise ValueError(msg)

            for param in text["params"]:
                if not isinstance(param, str):
                    msg = "Params are not all text-keys"
                    raise ValueError(msg)

            return StringToTranslate(
                wd=wd,
                key=text["key"],
                count=text["count"],
                params=text["params"],
            )
        else:
            msg = f'Unknown type "{t}"'
            raise ValueError(msg)
    except KeyError:
        msg = "Not enough information to unserialize"
        raise ValueError(msg) from None


async def render(
    text: TransText, request: Optional["Request"], multi_line=False
) -> Union[str, List[str]]:
    """
    Render either a normal string either a string to translate into an actual
    string for the specified request.
    """
    if isinstance(text, str):
        out = [text]
    elif isinstance(text, StringToTranslate):
        out = await text.render_list(request)
    else:
        msg = "Provided text cannot be rendered"
        raise TypeError(msg)

    if multi_line:
        return out
    else:
        return " ".join(out)
