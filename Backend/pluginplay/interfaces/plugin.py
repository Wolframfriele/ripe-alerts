import abc
import typing


class PluginInterface(abc.ABC):
    NAME = None
    DESCRIPTION = None
    DEFAULT_CONFIG = None

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def receiver(self, data: typing.Any) -> None:
        pass
