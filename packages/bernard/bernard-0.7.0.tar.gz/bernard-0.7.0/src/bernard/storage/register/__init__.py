from .base import BaseRegisterStore, Register  # noqa

try:  # noqa: SIM105
    # noinspection PyUnresolvedReferences
    from .redis import RedisRegisterStore  # noqa
except ImportError:
    pass
