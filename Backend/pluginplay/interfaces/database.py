import abc
import typing


class DatabaseInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def save_plugin_config(self, name: str, config: typing.Dict[str, typing.Any]) -> None:
        pass

    @abc.abstractmethod
    def get_plugin_config(self, name: str) -> typing.Union[typing.Dict[str, typing.Any], None]:
        pass

    @abc.abstractmethod
    def get_all_plugin_configs(self) -> typing.List[typing.Union[typing.Dict[str, typing.Any], None]]:
        pass
