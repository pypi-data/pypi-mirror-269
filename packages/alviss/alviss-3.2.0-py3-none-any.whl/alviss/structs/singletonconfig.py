__all__ = [
    "SingletonConfig",
]

from .baseconfig import *
from ccptools.structs import *


class SingletonConfig(BaseConfig, metaclass=Singleton):
    pass
