import asyncio
import logging
import time
from asyncio import Lock, sleep
from datetime import tzinfo
from hashlib import sha256
from typing import Any, ClassVar, Dict, List, Literal, Optional
from urllib.parse import quote, urljoin

import httpx
import jwt
import orjson
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from aiohttp.web_urldispatcher import UrlDispatcher
from sentry_sdk import capture_exception

from bernard import layers as lyr
from bernard.conf import settings
from bernard.core.health_check import HealthCheckFail
from bernard.engine.platform import PlatformOperationError
from bernard.engine.request import BaseMessage, Conversation, User
from bernard.engine.request import Request as BernardRequest
from bernard.engine.responder import Layers, Responder
from bernard.i18n import render
from bernard.layers import BaseLayer, Stack
from bernard.media.base import BaseMedia
from bernard.utils import patch_dict

from ...platforms import SimplePlatform
from ._utils import set_reply_markup
from .layers import (
    AnswerCallbackQuery,
    AnswerInlineQuery,
    BotCommand,
    InlineMessage,
    InlineQuery,
    Reply,
    Update,
)
from .media import Photo

TELEGRAM_URL = "https://api.telegram.org/bot{token}/{method}"

logger = logging.getLogger("bernard.platform.telegram")


class TelegramConversation(Conversation):
    """
    Matches the Telegram "chat" concept
    """

    def __init__(self, chat):
        self._chat = chat
        super().__init__(self._make_id())

    def _make_id(self):
        if "is_inline_query" in self._chat:
            return f'telegram:inline_query:{self._chat["id"]}'
        else:
            return f'telegram:conversation:{self._chat["id"]}'


class TelegramUser(User):
    def __init__(self, user, chat, telegram: "Telegram"):
        self._user = user
        self._chat = chat
        self._telegram = telegram
        self._full_user = None
        self._lock = Lock()
        super().__init__(self._make_id())

    def _make_id(self):
        return f'telegram:user:{self._user["id"]}'

    async def _get_full_user(self) -> Dict:
        """
        Sometimes Telegram does not provide all the user info with the message.
        In order to get the full profile (aka the language code) you need to
        call this method which will make sure that the full User object is
        loaded.

        The result is cached for the lifetime of the object, so if the function
        is called multiple times it will only fetch the user once. There is
        a locking mechanism around the cache to allow concurrent calls.
        """
        if "language_code" in self._user:
            return self._user

        async with self._lock:
            if self._full_user is None:
                cm = await self._telegram.call(
                    "getChatMember",
                    user_id=self._user["id"],
                    chat_id=self._chat["id"],
                )
                self._full_user = cm["result"]["user"]

            return self._full_user

    async def get_friendly_name(self) -> str:
        """
        Let's use the first name of the user as friendly name. In some cases
        the user object is incomplete, and in those cases the full user is
        fetched.
        """
        if "first_name" not in self._user:
            user = await self._get_full_user()
        else:
            user = self._user

        return user.get("first_name")

    async def get_locale(self) -> str:
        user = await self._get_full_user()
        return user.get("language_code", "")

    async def get_formal_name(self) -> str:
        parts = [
            self._user.get("first_name"),
            self._user.get("last_name"),
        ]

        return " ".join(x for x in parts if x)

    async def get_timezone(self) -> Optional[tzinfo]:
        return None

    async def get_full_name(self) -> str:
        return await self.get_formal_name()


class TelegramMessage(BaseMessage):
    def __init__(self, update: Dict, telegram: "Telegram"):
        self._update = update
        self._telegram = telegram

    def get_layers(self) -> List[BaseLayer]:
        out = []

        if "message" in self._update:
            msg = self._update.get("message", {})

            if "text" in msg:
                text = msg["text"]
                out.append(lyr.RawText(text))

                for entity in msg.get("entities") or []:
                    o = entity["offset"]
                    ln = entity["length"]
                    entity_text = text[o : o + ln]

                    if entity["type"] == "bot_command":
                        out.append(BotCommand(entity_text))

            if "reply_to_message" in msg:
                sub_msg = TelegramMessage(
                    {"message": msg["reply_to_message"]},
                    self._telegram,
                )
                out.append(lyr.Message(sub_msg))

            if "photo" in msg:
                media = Photo(msg["photo"])
                out.append(lyr.Image(media))

        if "callback_query" in self._update:
            payload = self._update["callback_query"]["data"]
            out.append(lyr.Postback(orjson.loads(payload)))
            out.append(InlineMessage())

            sub_msg = TelegramMessage(
                self._update["callback_query"],
                self._telegram,
            )
            out.append(lyr.Message(sub_msg))

        if "inline_query" in self._update:
            out.append(InlineQuery(self._update["inline_query"]))

        return out

    def get_platform(self) -> str:
        return self._telegram.NAME

    def _get_chat(self) -> Dict:
        """
        As Telegram changes where the chat object is located in the response,
        this method tries to be smart about finding it in the right place.
        """
        if "callback_query" in self._update:
            query = self._update["callback_query"]
            if "message" in query:
                return query["message"]["chat"]
            else:
                return {"id": query["chat_instance"]}
        elif "inline_query" in self._update:
            return patch_dict(
                self._update["inline_query"]["from"],
                is_inline_query=True,
            )
        elif "message" in self._update:
            return self._update["message"]["chat"]

    def _get_user(self) -> Dict:
        """
        Same thing as for `_get_chat()` but for the user related to the
        message.
        """
        if "callback_query" in self._update:
            return self._update["callback_query"]["from"]
        elif "inline_query" in self._update:
            return self._update["inline_query"]["from"]
        elif "message" in self._update:
            return self._update["message"]["from"]

    def get_conversation(self) -> Conversation:
        return TelegramConversation(self._get_chat())

    def get_user(self) -> User:
        return TelegramUser(self._get_user(), self._get_chat(), self._telegram)

    def get_chat_id(self) -> str:
        return self._get_chat()["id"]

    async def get_token(self) -> str:
        user = self.get_user()
        # noinspection PyUnresolvedReferences,PyProtectedMember
        user_id = user._user["id"]
        # noinspection PyUnresolvedReferences,PyProtectedMember
        chat_id = user._chat["id"]

        return jwt.encode(
            {
                "telegram_user_id": user_id,
                "telegram_chat_id": chat_id,
            },
            settings.WEBVIEW_SECRET_KEY,
            algorithm=settings.WEBVIEW_JWT_ALGORITHM,
        )


class TelegramResponder(Responder):
    """
    This responder handles most of the magic behind Telegram messages
    acknowledgements and so on.
    """

    platform: "Telegram"

    def __init__(self, update, platform):
        super().__init__(platform)

        self._update = update

        if "callback_query" in update:
            self._acq = AnswerCallbackQuery()
        else:
            self._acq = None

    def send(self, stack: Layers):
        """
        Intercept any potential "AnswerCallbackQuery" before adding the stack
        to the output buffer.
        """
        if not isinstance(stack, Stack):
            stack = Stack(stack)

        self._send_update(stack)
        stack = self._send_answer(stack)
        self._send_reply(stack)
        self._send_inline_query(stack)

        if stack.layers:
            return super().send(stack)

    def _send_update(self, stack):
        if "callback_query" in self._update and stack.has_layer(Update):
            layer = stack.get_layer(Update)

            try:
                msg = self._update["callback_query"]["message"]
            except KeyError:
                layer.inline_message_id = self._update["callback_query"][
                    "inline_message_id"
                ]
            else:
                layer.chat_id = msg["chat"]["id"]
                layer.message_id = msg["message_id"]

    def _send_answer(self, stack):
        if stack.has_layer(AnswerCallbackQuery):
            self._acq = stack.get_layer(AnswerCallbackQuery)

            stack = Stack(
                [
                    layer
                    for layer in stack.layers
                    if not isinstance(layer, AnswerCallbackQuery)
                ]
            )

        return stack

    def _send_reply(self, stack):
        if stack.has_layer(Reply):
            layer = stack.get_layer(Reply)

            if "message" in self._update:
                layer.message = self._update["message"]
            elif "callback_query" in self._update:
                layer.message = self._update["callback_query"]["message"]

    def _send_inline_query(self, stack):
        if "inline_query" in self._update and stack.has_layer(AnswerInlineQuery):
            a = stack.get_layer(AnswerInlineQuery)
            a.inline_query_id = self._update["inline_query"]["id"]

    async def flush(self, request: BernardRequest):
        """
        If there's a AnswerCallbackQuery scheduled for reply, place the call
        before actually flushing the buffer.
        """
        if self._acq and "callback_query" in self._update:
            try:
                cbq_id = self._update["callback_query"]["id"]
            except KeyError:
                pass
            else:
                await self.platform.call(
                    "answerCallbackQuery", **(await self._acq.serialize(cbq_id))
                )

        return await super().flush(request)


class Telegram(SimplePlatform):
    NAME = "telegram"
    PATTERNS: ClassVar[dict[str, str]] = {
        "plain_text": "^(Text|RawText|MultiText)+ "
        "(InlineKeyboard|ReplyKeyboard|ReplyKeyboardRemove)? "
        "Reply?$"
        "|^(Text|RawText) InlineKeyboard? Reply? Update$",
        "inline_answer": "^AnswerInlineQuery$",
        "markdown": "^Markdown+ "
        "(InlineKeyboard|ReplyKeyboard|ReplyKeyboardRemove)? "
        "Reply?$"
        "|^Markdown InlineKeyboard? Reply? Update$",
        "sleep": "^Sleep$",
        "typing": "^Typing$",
    }

    def __init__(self):
        super().__init__()
        self._polling_t = None

    @classmethod
    async def self_check(cls):
        """
        Check that the configuration is correct

        - Presence of "token" in the settings
        - Presence of "BERNARD_BASE_URL" in the global configuration
        """
        # noinspection PyTypeChecker
        async for check in super().self_check():
            yield check

        s = cls.settings()

        try:
            if not isinstance(s["token"], str):
                raise AssertionError
        except (KeyError, TypeError, AssertionError):
            yield HealthCheckFail(
                "00005",
                'Missing "token" for Telegram platform. You can obtain one by'
                "registering your bot in Telegram.",
            )

        if not hasattr(settings, "BERNARD_BASE_URL"):
            yield HealthCheckFail(
                "00005",
                '"BERNARD_BASE_URL" cannot be found in the configuration. The'
                "Telegram platform needs it because it uses it to "
                "automatically register its hook.",
            )

        if not hasattr(settings, "WEBVIEW_SECRET_KEY"):
            yield HealthCheckFail(
                "00005",
                '"WEBVIEW_SECRET_KEY" cannot be found in the configuration. '
                "It is required in order to be able to create secure postback "
                "URLs.",
            )

    @property
    def telegram_update_mode(self) -> Literal["polling", "webhook"]:
        """Determining from settings how we are supposed to receive updates.

        Telegram supports two modes: either the webhook, which calls an HTTP
        hook on your behalf, which is good at scale if you want to have several
        servers answer requests etc. But this framework is pretty lightweight,
        so before you need to scale horizontally there is probably a lot of
        time that will pass.

        Instead, the recommended way for most people is to use the polling
        method. The huge advantage of it is that you don't need a public URL
        for your bot, so it's ideal for development environments. The only
        drawback is that you can't scale horizontally with it.
        """

        return self.settings().get("update_mode", "polling")

    def hook_up(self, router: UrlDispatcher):
        if self.telegram_update_mode == "webhook":
            router.add_post(self.make_hook_path(), self.receive_updates)

    async def _poll_updates(self):
        """Using the poll method for Telegram updates.

        It's very simple, you just call the same endpoint repeatedly until you
        get an answer, this forever and ever.
        """

        min_time = 1
        offset = 0

        while True:
            time_start = time.time()

            try:
                updates = await self.call(
                    "getUpdates",
                    _log=False,
                    offset=offset,
                    timeout=5,
                    allowed_updates=[
                        "message",
                        "callback_query",
                        "inline_query",
                    ],
                )

                for update in updates["result"]:
                    message = TelegramMessage(update, self)
                    responder = TelegramResponder(update, self)
                    await self._notify(message, responder)

                if updates["result"]:
                    offset = max(x["update_id"] for x in updates["result"]) + 1
            except httpx.ReadTimeout:
                pass
            except Exception as e:
                capture_exception(e)
                logger.exception("Error while polling Telegram: %s")

            time_end = time.time()
            time_diff = time_end - time_start

            if time_diff < min_time:
                await sleep(min_time - time_diff)

    async def receive_updates(self, request: Request):
        """
        Handle updates from Telegram
        """
        body = await request.read()

        try:
            content = orjson.loads(body)
        except ValueError:
            return json_response(
                {
                    "error": True,
                    "message": "Cannot decode body",
                },
                status=400,
            )

        logger.debug("Received from Telegram: %s", content)

        message = TelegramMessage(content, self)
        responder = TelegramResponder(content, self)
        await self._notify(message, responder)

        return json_response(
            {
                "error": False,
            }
        )

    async def message_from_token(
        self, token: str, payload: Any
    ) -> Optional[BaseMessage]:
        try:
            tk = jwt.decode(token, settings.WEBVIEW_SECRET_KEY)
        except jwt.InvalidTokenError:
            return None

        try:
            user_id = tk["telegram_user_id"]

            if not isinstance(user_id, int):
                raise AssertionError

            chat_id = tk["telegram_chat_id"]

            if not isinstance(chat_id, int):
                raise AssertionError
        except (KeyError, AssertionError):
            return None

        fake_message = {
            "callback_query": {
                "from": {
                    "id": user_id,
                },
                "message": {
                    "chat": {
                        "id": chat_id,
                    },
                },
                "data": orjson.dumps(payload).decode(),
            }
        }

        return TelegramMessage(fake_message, self)

    async def inject_message(self, message: TelegramMessage) -> None:
        # noinspection PyProtectedMember
        responder = TelegramResponder(message._update, self)
        await self._notify(message, responder)

    def make_url(self, method):
        """
        Generate a Telegram URL for this bot.
        """
        token = self.settings()["token"]

        return TELEGRAM_URL.format(
            token=quote(token),
            method=quote(method),
        )

    async def call(
        self,
        method: str,
        _ignore: set[str] | None = None,
        _log: bool = True,
        **params: Any,
    ):
        """
        Call a telegram method

        :param _ignore: List of reasons to ignore
        :param _log: Whether to log the call or not
        :param method: Name of the method to call
        :param params: Dictionary of the parameters to send

        :return: Returns the API response
        """
        if _log:
            logger.debug("Calling Telegram %s(%s)", method, params)

        url = self.make_url(method)

        headers = {
            "content-type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            r = await client.post(
                url,
                json=params,
                headers=headers,
            )
            out = await self._handle_telegram_response(r, _ignore)

            if _log:
                logger.debug("Telegram replied: %s", out)

            return out

    async def _handle_telegram_response(self, response: httpx.Response, ignore=None):
        """
        Parse a response from Telegram. If there's an error, an exception will
        be raised with an explicative message.

        :param response: Response to parse
        :return: Data
        """
        if ignore is None:
            ignore = set()

        ok = response.status_code == 200

        try:
            data = response.json()

            if not ok:
                desc = data["description"]

                if desc in ignore:
                    return None

                msg = f"Telegram replied with an error: {desc}"
                raise PlatformOperationError(msg)
        except (ValueError, TypeError, KeyError):
            msg = "An unknown Telegram error occurred"
            raise PlatformOperationError(msg) from None

        return data

    def make_hook_path(self):
        """
        Compute the path to the hook URL
        """
        token = self.settings()["token"]
        h = sha256()
        h.update(token.encode())
        key = str(h.hexdigest())
        return f"/hooks/telegram/{key}"

    async def _deferred_init(self):
        """
        Make sure that the webhook is in the required state. In case of polling
        the webhook is disabled and a polling task is started, in case of
        webhook the webhook is set.
        """
        if self.telegram_update_mode == "webhook":
            hook_path = self.make_hook_path()
            url = urljoin(settings.BERNARD_BASE_URL, hook_path)
            await self.call("setWebhook", url=url)
            logger.info('Setting Telegram webhook to "%s"', url)
        else:
            info = await self.call("getWebhookInfo")

            if url := info["result"]["url"]:
                logger.info(
                    (
                        'Telegram webhook is set to "%s", disabling it '
                        "because polling is enabled"
                    ),
                    url,
                )
                await self.call("deleteWebhook")

            self._polling_t = asyncio.create_task(self._poll_updates())

    async def _send_text(
        self, request: Request, stack: Stack, parse_mode: Optional[str] = None
    ):
        """
        Base function for sending text
        """
        parts = []
        chat_id = request.message.get_chat_id()

        for layer in stack.layers:
            if isinstance(layer, (lyr.Text, lyr.RawText, lyr.Markdown)):
                text = await render(layer.text, request)
                parts.append(text)
            elif isinstance(layer, lyr.MultiText):
                lines = await render(layer.text, request, multi_line=True)
                parts.extend(lines)

        for part in parts[:-1]:
            await self.call(
                "sendMessage",
                text=part,
                chat_id=chat_id,
            )

        msg = {
            "text": parts[-1],
            "chat_id": chat_id,
        }

        if parse_mode is not None:
            msg["parse_mode"] = parse_mode

        await set_reply_markup(msg, request, stack)

        if stack.has_layer(Reply):
            reply = stack.get_layer(Reply)
            if reply.message:
                msg["reply_to_message_id"] = reply.message["message_id"]

        if stack.has_layer(Update):
            update = stack.get_layer(Update)

            if update.inline_message_id:
                msg["inline_message_id"] = update.inline_message_id
                del msg["chat_id"]
            else:
                msg["message_id"] = update.message_id

            await self.call(
                "editMessageText", {"Bad Request: message is not modified"}, **msg
            )
        else:
            await self.call("sendMessage", **msg)

    async def _send_plain_text(self, request: Request, stack: Stack):
        """
        Sends plain text using `_send_text()`.
        """
        await self._send_text(request, stack, None)

    async def _send_markdown(self, request: Request, stack: Stack):
        """
        Sends Markdown using `_send_text()`
        """
        await self._send_text(request, stack, "Markdown")

    async def _send_sleep(self, request: Request, stack: Stack):
        """
        Sleep for the amount of time specified in the Sleep layer
        """
        duration = stack.get_layer(lyr.Sleep).duration
        await sleep(duration)

    async def _send_inline_answer(self, request: Request, stack: Stack):
        aiq = stack.get_layer(AnswerInlineQuery)
        answer = await aiq.serialize(request)
        await self.call("answerInlineQuery", **answer)

    async def _send_typing(self, request: Request, stack: Stack):
        """
        In telegram, the typing stops when the message is received. Thus, there
        is no "typing stops" messages to send. The API is only called when
        typing must start.
        """
        t = stack.get_layer(lyr.Typing)

        if t.active:
            await self.call(
                "sendChatAction",
                chat_id=request.message.get_chat_id(),
                action="typing",
            )

    def ensure_usable_media(self, media: BaseMedia) -> BaseMedia:
        raise NotImplementedError
