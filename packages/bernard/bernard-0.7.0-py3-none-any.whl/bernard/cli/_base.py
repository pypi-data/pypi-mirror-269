import logging

from rich.logging import RichHandler

logger = logging.getLogger("bernard.cli")
_tasks = set()


def init_logger():
    import logging

    logging.basicConfig(
        level=logging.WARNING,
        format=r"[bold cyan]\[%(name)s][/] %(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(markup=True)],
    )
    logging.getLogger("watchdog.observers").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


async def init_live_reload(run):
    """
    Start the live reload task

    :param run: run the task inside of this function or just create it
    """
    from asyncio import get_event_loop

    from ._live_reload import start_child

    loop = get_event_loop()

    if run:
        await start_child()
    else:
        t = loop.create_task(start_child())
        _tasks.add(t)
        t.add_done_callback(_tasks.discard)


async def run_core():
    import asyncio

    from aiohttp import web

    from bernard.conf import settings
    from bernard.platforms import start_all
    from bernard.server import app

    try:
        await start_all()

        web_t = asyncio.create_task(web._run_app(app, **settings.SERVER_BIND))

        if settings.CODE_LIVE_RELOAD:
            await init_live_reload(False)

        await web_t
    except Exception:
        logger.exception("Error while running core")

        if settings.CODE_LIVE_RELOAD:
            await init_live_reload(True)


def main():
    init_logger()

    import asyncio
    from os import getenv

    from bernard.conf import settings

    if settings.DEBUG:
        logging.root.setLevel(logging.DEBUG)

    if settings.CODE_LIVE_RELOAD and getenv("_IN_CHILD") != "yes":
        from ._live_reload import start_parent

        return start_parent()

    asyncio.run(run_core())
