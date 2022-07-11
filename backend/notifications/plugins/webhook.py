from multiprocessing.sharedctypes import Value
from ..pluginplay.interfaces import plugin as plugin
import typing
import requests
import json


class WebhookPlugin(plugin.PluginInterface):
    NAME = "Webhook"
    DESCRIPTION = "This plugin is meant to send message to webhooks"
    DEFAULT_CONFIG = {"URL": "http://localhost:8000"}

    def __init__(self, config: typing.Dict[str, typing.Any]) -> None:
        if not config:
            print("No config avaliable")
            data = '{"url":"http://localhost:8000"}'
            self.config_data = json.loads(data)
        else:
            self.config_data = getattr(config, "config", config)

    def receiver(self, message: str) -> None:
        config = json.loads(self.config_data)
        if not message:
            print("No message avaliable!")
        else:
            requests.post(config['url'], data=json.dumps(message), headers={'Content-Type': 'application/json'})
