from ..pluginplay.interfaces import plugin as plugin
import typing


class PrintPlugin(plugin.PluginInterface):
    NAME = "Webhook plugin"
    DESCRIPTION = "This plugin is meant to send message to webhooks"
    DEFAULT_CONFIG = {"URL": "Hello world!"}

    def __init__(self, config: typing.Dict[str, typing.Any]) -> None:
        #print(config)
        pass

    def receiver(self, message: str) -> None:
        print(f"(Webhook message): {message}")