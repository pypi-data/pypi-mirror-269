from typing import Type  # noqa

from ..engine.platform import Platform, SimplePlatform  # noqa
from ..utils import import_class  # noqa
from .management import PlatformManager, get_platform_settings  # noqa

manager = PlatformManager()


async def start_all():
    """
    A utility function for the CLI to start all platforms directly and not
    lazily wait for them to start.
    """
    await manager.init()

    async for _ in manager.get_all_platforms():
        pass
