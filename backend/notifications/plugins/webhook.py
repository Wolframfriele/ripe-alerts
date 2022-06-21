from multiprocessing.sharedctypes import Value
from ..pluginplay.interfaces import plugin as plugin
import typing
import requests
import json


class WebhookPlugin(plugin.PluginInterface):
    NAME = "Webhook"
    DESCRIPTION = "This plugin is meant to send message to webhooks"
    DEFAULT_CONFIG = {"URL": "Hello world!"}

    def __init__(self, config: typing.Dict[str, typing.Any]) -> None:
        self.config = config.config
        pass

    def receiver(self, message: str) -> None:
        config = json.loads(self.config)
        data = { 'Alert': 'There was a anomaly found in your network' }
        requests.post(config['url'], data=json.dumps(data), headers={'Content-Type': 'application/json'})