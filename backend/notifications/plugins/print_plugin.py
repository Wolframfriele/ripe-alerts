from ..pluginplay.interfaces import plugin as plugin
import typing


class PrintPlugin(plugin.PluginInterface):
    NAME = "Print alert plugin"
    DESCRIPTION = "This plugin outputs to STDOUT"
    DEFAULT_CONFIG = {"Text": "Hello world!"}

    def __init__(self, config: typing.Dict[str, typing.Any]) -> None:
        #print(config)
        pass

    def receiver(self, message: str) -> None:
        print(f"(Print): {message}")
